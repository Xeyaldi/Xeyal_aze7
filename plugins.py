import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from motor.motor_asyncio import AsyncIOMotorClient

# --- MONDODB BAĞLANTISI (Sənin Stats Kodundan) ---
MONGO_URL = os.environ.get("MONGO_DB_URI")
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db["PersistentStats"]
stats_col = db["group_stats"]

# --- MƏLUMAT BAZASI & KARMA (Köhnə Koddan) ---
user_karma = {} 

# --- ADMİN YOXLAMA ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- MENTION FUNKSİYASI ---
async def get_mention(client, user_input):
    try:
        user = await client.get_users(user_input)
        return f"[{user.first_name}](tg://user?id={user.id})"
    except: return f"`{user_input}`"

# --- 🏆 SIRALAMA GÖSTƏRİCİSİ (Sənin 13 nəfərlik reytinqin) ---
async def get_stats_display(chat_id, user_id, user_nick, key, title):
    top_13 = stats_col.find({"chat_id": chat_id, key: {"$gt": 0}}).sort(key, -1).limit(13)
    my_data = await stats_col.find_one({"chat_id": chat_id, "user_id": user_id})
    my_count = my_data[key] if my_data else 0
    
    res_text = f"<b>🚀 {title} Aktivlik Reytinqi (Top 13)</b>\n\n"
    res_text += "<b>İstifadəçi ✨ Mesaj</b>\n"
    res_text += "──────────────────\n"
    
    count = 1
    async for user in top_13:
        if count == 1: marker = "🥇"
        elif count == 2: marker = "🥈"
        elif count == 3: marker = "🥉"
        else: marker = "🎗️"
        u_name = user.get('name') or f"User_{user['user_id']}"
        res_text += f"{marker} {count}. <b>{u_name}</b> ➜ <code>{user.get(key, 0)}</code>\n"
        count += 1
    
    res_text += "──────────────────\n"
    res_text += f"👤 <b>Sənin {user_nick} :</b> <code>{my_count}</code> mesaj"
    return res_text

# --- ⌨️ BUTONLAR (Sənin emojilərin) ---
def gen_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Günlük", callback_data="p_daily"), 
         InlineKeyboardButton("📈 Həftəlik", callback_data="p_weekly")],
        [InlineKeyboardButton("🌟 Aylıq", callback_data="p_monthly"), 
         InlineKeyboardButton("🌍 Ümumi", callback_data="p_total")],
        [InlineKeyboardButton("✖️ Siyahını Bağla", callback_data="close_stats")]
    ])

# --- 🚀 İNİT FUNKSİYASI ---
def init_plugins(app, get_db_connection, user_app=None):
    OWNERS = [6241071228, 7592728364, 8024893255]
    TARGET_GROUP = "@sohbetqruprc"

    # --- 📈 AVTO-TREK (Stats Yaddaşı) ---
    @app.on_message(filters.group & ~filters.bot, group=1)
    async def track_bot_msg(_, message):
        if not message.from_user: return
        await stats_col.update_one(
            {"chat_id": message.chat.id, "user_id": message.from_user.id},
            {"$inc": {"daily": 1, "weekly": 1, "monthly": 1, "total": 1},
             "$set": {"name": message.from_user.first_name}}, upsert=True)

    if user_app:
        @user_app.on_message(filters.group & ~filters.bot, group=1)
        async def track_user_msg(_, message):
            if not message.from_user: return
            await stats_col.update_one(
                {"chat_id": message.chat.id, "user_id": message.from_user.id},
                {"$inc": {"daily": 1, "weekly": 1, "monthly": 1, "total": 1},
                 "$set": {"name": message.from_user.first_name}}, upsert=True)

    # --- 🏆 TOPSIRALAMA & CALLBACKS ---
    @app.on_message(filters.command(["topsiralama", "stats"]) & filters.group)
    async def show_stats(client, message):
        text = await get_stats_display(message.chat.id, message.from_user.id, message.from_user.first_name, "daily", "Bugün")
        await message.reply_text(text, reply_markup=gen_buttons())

    @app.on_callback_query(filters.regex(r"^p_"))
    async def handle_stats_buttons(client, query):
        p_type = query.data.split("_")[1]
        titles = {"daily": "Bugün", "weekly": "Bu Həftə", "monthly": "Bu Ay", "total": "Ümumi"}
        updated_text = await get_stats_display(query.message.chat.id, query.from_user.id, query.from_user.first_name, p_type, titles.get(p_type))
        try: await query.message.edit_text(updated_text, reply_markup=gen_buttons())
        except: pass

    @app.on_callback_query(filters.regex("close_stats"))
    async def _close(_, query):
        await query.message.delete()

    # --- GLOBAL HANDLER (Karma +/-) ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def global_handler(client, message):
        if not message.from_user or not message.reply_to_message: return
        c_id, u_id = message.chat.id, message.from_user.id
        target_id = message.reply_to_message.from_user.id
        if target_id == u_id: return
        if c_id not in user_karma: user_karma[c_id] = {}
        if message.text == "+":
            user_karma[c_id][target_id] = user_karma[c_id].get(target_id, 0) + 1
            await message.reply_text(f"➕ **{message.reply_to_message.from_user.first_name}** karması artdı!")
        elif message.text == "-":
            user_karma[c_id][target_id] = user_karma[c_id].get(target_id, 0) - 1
            await message.reply_text(f"➖ **{message.reply_to_message.from_user.first_name}** karması azaldı!")

    # --- 🤫 ETİRAF SİSTEMİ ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_handler(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        sender = "Anonim" if message.command[0] == "etiraf" else message.from_user.first_name
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data="acc_et")]])
        for o in OWNERS:
            try: await client.send_message(o, f"📩 Etiraf: `{txt}`\n👤 Kimdən: {sender}", reply_markup=btn)
            except: pass
        await message.reply_text("✅ Etirafınız moderatorlara göndərildi.")

    @app.on_callback_query(filters.regex("acc_et"))
    async def acc_callback(client, callback_query):
        try:
            etiraf_txt = callback_query.message.text.split('📩 Etiraf: ')[1].split('👤 Kimdən:')[0]
            await client.send_message(TARGET_GROUP, f"🤫 **Etiraf:**\n\n{etiraf_txt}")
            await callback_query.edit_message_text("✅ Təsdiqləndi.")
        except: pass

    # --- 🖼 MULTIMEDIA (Ağ-Qara & PDF) ---
    @app.on_message(filters.photo & filters.group)
    async def bw_photo(client, message):
        path = await message.download()
        with Image.open(path) as img: img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Ağ-qara edildi.")
        if os.path.exists(path): os.remove(path); os.remove("bw.jpg")

    @app.on_message(filters.command("pdf"))
    async def instant_pdf(client, message):
        if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
        target = message.reply_to_message
        photo_path = await target.download() if target.photo else None
        text_content = target.caption if target.photo else (target.text if target.text else None)
        pdf_name = f"pdf_{message.from_user.id}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        if photo_path:
            with Image.open(photo_path) as img: img.convert("L").save(photo_path)
            c.drawImage(photo_path, 50, 350, 500, 450); os.remove(photo_path)
        if text_content:
            c.setFont("Helvetica", 14); c.drawString(70, 320 if photo_path else 800, f"Mezmun: {text_content[:150]}")
        c.save()
        await message.reply_document(pdf_name, caption="📄 PDF hazırdır!"); os.remove(pdf_name)

    # --- 💖 ƏYLƏNCƏ (Love, Slap, Games) ---
    @app.on_message(filters.command("love"))
    async def love_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target)
        p = int(hashlib.md5(f"{message.from_user.id}{target}".encode()).hexdigest(), 16) % 101
        await message.reply_text(f"💘 {u2} ilə uyğunluq: `{p}%`")

    @app.on_message(filters.command("slap"))
    async def slap_cmd(client, message):
        if message.reply_to_message: await message.reply_text(f"🥊 **{message.reply_to_message.from_user.first_name}** şapalaqlandı!")

    @app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
    async def games(client, message):
        em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
        await client.send_dice(message.chat.id, emoji=em[message.command[0]])

    # --- 📚 HELP, ID, WIKI, QR ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        await message.reply_text("<b>╔═══════ 💠 BOT PRO 💠 ═══════╗</b>\n➜ <code>/topsiralama</code>\n➜ <code>/love</code>, <code>/slap</code>\n➜ <code>/pdf</code>, <code>/qr</code>\n<b>╚══════════════════════════╝</b>")

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message): await message.reply_text(f"🆔 ID: `{message.from_user.id}`")

    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        if len(message.command) < 2: return
        wikipedia.set_lang("az")
        try: await message.reply_text(f"📖 {wikipedia.summary(message.text.split(None, 1)[1], sentences=2)}")
        except: pass

    @app.on_message(filters.command("qr"))
    async def qr_cmd(client, message):
        if len(message.command) < 2: return
        txt = urllib.parse.quote(message.text.split(None, 1)[1])
        await message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}")
