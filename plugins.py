import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- MƏLUMAT BAZASI SİMULYASİYASI ---
user_stats = {} 

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

# --- RÜTBƏ TƏYİNİ ---
def get_rank(count):
    if count > 10000: return "💎 Marşal"
    if count > 5000: return "🌟 General"
    if count > 2000: return "🎖️ Polkovnik"
    if count > 1000: return "🎖️ Mayor"
    if count > 50: return "🔫 Çavuş"
    return "🛡️ Sıravi"

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    TARGET_GROUP = "@sohbetqruprc"

    # --- KOMANDALARIN MENYUSU (SƏS ÇIXARILDI) ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Geniş kömək menyusu"),
            BotCommand("topsiralama", "🎖️ Rütbə sıralaması (Top 20)"),
            BotCommand("skan", "🔍 Köhnə mesajları analiz et"),
            BotCommand("pdf", "📄 Mesajı dərhal PDF et (Reply)"),
            BotCommand("kripto", "🪙 Kripto kursları"),
            BotCommand("love", "💘 Sevgi testi"),
            BotCommand("slap", "🥊 Şapalaq"),
            BotCommand("qr", "🖼 QR kod yaradar"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("valyuta", "💰 Məzənnələr"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("etiraf", "🤫 Anonim etiraf"),
            BotCommand("id", "🆔 ID-ləri göstərər"),
            BotCommand("purge", "🧹 Mesajları silər")
        ]
        await app.set_bot_commands(commands)

    # --- MESAJ SAYĞACI ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def count_messages(client, message):
        c_id, u_id = message.chat.id, message.from_user.id
        if c_id not in user_stats: user_stats[c_id] = {}
        user_stats[c_id][u_id] = user_stats[c_id].get(u_id, 0) + 1

    # --- 🔍 KÖHNƏ MESAJLARI SKAN ETMƏK ---
    @app.on_message(filters.command("skan") & filters.group)
    async def scan_history(client, message):
        if not await check_admin(client, message, OWNERS):
            return await message.reply_text("❌ Bu komanda yalnız adminlər üçündür.")
        
        m_wait = await message.reply_text("🔍 Qrup tarixçəsi skan edilir, köhnə mesajlar hesablanır...")
        c_id = message.chat.id
        if c_id not in user_stats: user_stats[c_id] = {}

        async for msg in client.get_chat_history(c_id, limit=5000):
            if msg.from_user and not msg.from_user.is_bot:
                u_id = msg.from_user.id
                user_stats[c_id][u_id] = user_stats[c_id].get(u_id, 0) + 1
        
        await m_wait.edit("✅ Skan tamamlandı! Köhnə mesajlar rütbələrə əlavə edildi.")

    # --- 📚 HELP MENYU (SƏS ŞEYLƏRİ TAM ÇIXARILDI) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **B O T  F U L L  M E N Y U** 💠\n"
            "╚════════════════════╝\n\n"
            "🎖️ **Rütbə Sistemi:**\n"
            "🔹 `/topsiralama` - Qrupun Top 20 əsgəri.\n"
            "🔹 `/skan` - Əvvəlki mesajları rütbəyə salar.\n\n"
            "📄 **Super PDF:**\n"
            "🔹 Mesaja reply verib `/pdf` yazın. Şəkil və mətni dərhal PDF edər.\n\n"
            "🖼 **Şəkil Aləti:**\n"
            "🔹 Şəkil göndərin - Bot onu ağ-qara edəcək.\n\n"
            "💖 **Əyləncə:**\n"
            "🔹 `/love`, `/slap`, `/dice`, `/slot`, `/futbol`, `/basket`.\n\n"
            "🌍 **Məlumat:**\n"
            "🔹 `/kripto`, `/wiki`, `/valyuta`, `/namaz`, `/qr`.\n\n"
            "🤫 **Etiraf:**\n"
            "🔹 `/etiraf` / `/acetiraf` - Moderator təsdiqli.\n\n"
            "🛠 **Admin:**\n"
            "🔹 `/purge`, `/id`, `/info`.\n"
        )
        await message.reply_text(help_text)

    # --- 🎖️ TOPSIRALAMA (TOP 20) ---
    @app.on_message(filters.command("topsiralama") & filters.group)
    async def top_ranks(client, message):
        c_id = message.chat.id
        if c_id not in user_stats or not user_stats[c_id]:
            return await message.reply_text("🪖 Məlumat yoxdur. `/skan` yazın.")
        
        sorted_users = sorted(user_stats[c_id].items(), key=lambda x: x[1], reverse=True)[:20]
        text = "🎖️ **Qrupun Ən Aktiv 20 Əsgəri** 🎖️\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, count) in enumerate(sorted_users, 1):
            mention = await get_mention(client, u_id)
            rank = get_rank(count)
            text += f"{i:02d}. {rank} | {mention}\n╰─ 💬 Mesaj: `{count}`\n\n"
        await message.reply_text(text)

    # --- 📄 PDF (DƏRHAL) ---
    @app.on_message(filters.command("pdf"))
    async def instant_pdf(client, message):
        if not message.reply_to_message:
            return await message.reply_text("❌ PDF üçün mesaja reply verin!")
        
        target = message.reply_to_message
        photo_path = await target.download() if target.photo else None
        text_content = target.caption if target.photo else (target.text if target.text else None)

        wait_msg = await message.reply_text("⏳ PDF hazırlanır...")
        pdf_name = f"pdf_{message.from_user.id}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        
        if photo_path:
            with Image.open(photo_path) as img:
                img.convert("L").save(photo_path)
            c.drawImage(photo_path, 50, 350, 500, 450)
            os.remove(photo_path)
            
        if text_content:
            c.setFont("Helvetica", 14)
            y_pos = 320 if photo_path else 800
            c.drawString(70, y_pos, f"Metn: {text_content[:150]}...")

        c.showPage(); c.save()
        await message.reply_document(pdf_name, caption="📄 PDF hazırdır!")
        os.remove(pdf_name); await wait_msg.delete()

    # --- 🤫 ETİRAF ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_handler(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        sender = "Anonim" if message.command[0] == "etiraf" else message.from_user.first_name
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data="acc_et")]])
        for o in OWNERS: await client.send_message(o, f"📩 Etiraf: `{txt}`\n👤 Kimdən: {sender}", reply_markup=btn)
        await message.reply_text("✅ Moderatorlara göndərildi.")

    @app.on_callback_query(filters.regex("acc_et"))
    async def acc_callback(client, callback_query):
        await client.send_message(TARGET_GROUP, f"🤫 **Etiraf:**\n\n{callback_query.message.text}")
        await callback_query.edit_message_text("✅ Təsdiqləndi.")

    # --- 🖼 ŞƏKİL REDAKTORU ---
    @app.on_message(filters.photo)
    async def bw_photo(client, message):
        path = await message.download()
        with Image.open(path) as img: img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Ağ-qara edildi.")
        os.remove(path); os.remove("bw.jpg")

    # --- DİGƏR ---
    @app.on_message(filters.command("kripto"))
    async def crypto_cmd(client, message):
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]").json()
        await message.reply_text(f"🪙 BTC: `${float(r[0]['price']):,.2f}`\n💠 ETH: `${float(r[1]['price']):,.2f}`")

    @app.on_message(filters.command("valyuta"))
    async def val_cmd(client, message):
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 USD: `{1/r['rates']['USD']:.2f}` AZN")

    @app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
    async def games(client, message):
        em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
        await client.send_dice(message.chat.id, emoji=em[message.command[0]])

    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        ids = list(range(message.reply_to_message.id, message.id))
        for i in range(0, len(ids), 100): await client.delete_messages(message.chat.id, ids[i:i+100])

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message):
        await message.reply_text(f"🆔 Sizin ID: `{message.from_user.id}`\n🆔 Çat ID: `{message.chat.id}`")
