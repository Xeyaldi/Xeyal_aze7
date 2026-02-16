import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- MƏLUMAT BAZASI & KARMA ---
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

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    TARGET_GROUP = "@sohbetqruprc"

    # --- GLOBAL HANDLER (Karma & Orijinal Reaksiyalar) ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def global_handler(client, message):
        if not message.from_user: return
        c_id, u_id = message.chat.id, message.from_user.id
        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            if target_id == u_id: return
            if c_id not in user_karma: user_karma[c_id] = {}
            if message.text == "+":
                user_karma[c_id][target_id] = user_karma[c_id].get(target_id, 0) + 1
                await message.reply_text(f"➕ **{message.reply_to_message.from_user.first_name}** karması artdı!")
            elif message.text == "-":
                user_karma[c_id][target_id] = user_karma[c_id].get(target_id, 0) - 1
                await message.reply_text(f"➖ **{message.reply_to_message.from_user.first_name}** karması azaldı!")

    # --- 📚 HELP MENYU ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "<b>╔═══════ 💠 BOT PRO 💠 ═══════╗</b>\n\n"
            "🏆 <b>REYТİNQ & VİZYON:</b>\n"
            "➜ <code>/topsiralama</code>, <code>/proqnoz</code>, <code>/qizilfond</code>\n\n"
            "🌍 <b>TƏRCÜMƏ SİSTEMİ:</b>\n"
            "➜ Mesaja reply verib: <code>/traz</code>, <code>/tren</code>, <code>/trru</code>...\n\n"
            "📄 <b>MULTİMEDİA:</b>\n"
            "➜ <code>/pdf</code> : Şəkil/Mətni PDF edər.\n"
            "➜ <code>/qr [mətn]</code> : QR kod yaradar.\n"
            "➜ <b>Şəkil göndər</b> : Avtomatik ağ-qara effekt.\n\n"
            "💰 <b>MƏLUMAT:</b>\n"
            "➜ <code>/kripto</code>, <code>/valyuta</code>, <code>/wiki</code>, <code>/namaz</code>.\n\n"
            "💖 <b>ƏYLƏNCƏ:</b>\n"
            "➜ <code>/love</code>, <code>/slap</code>, <code>/dice</code>, <code>/slot</code>, <code>/futbol</code>, <code>/basket</code>.\n\n"
            "🛠 <b>SİSTEM & ADMİN:</b>\n"
            "➜ <code>/id</code>, <code>/purge</code>, <code>/etiraf</code>.\n"
            "<b>╚══════════════════════════╝</b>"
        )
        await message.reply_text(help_text)

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

    # --- 🖼 AĞ-QARA ŞƏKİL EFFEKTİ ---
    @app.on_message(filters.photo & filters.group)
    async def bw_photo(client, message):
        path = await message.download()
        with Image.open(path) as img:
            img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Ağ-qara edildi.")
        if os.path.exists(path): os.remove(path)
        if os.path.exists("bw.jpg"): os.remove("bw.jpg")

    # --- 🔤 TƏRCÜMƏ ---
    @app.on_message(filters.command(["tercume", "traz", "tren", "trru", "trtr", "trde", "trfr"]))
    async def multi_translate(client, message):
        if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text: return
        cmd = message.command[0].lower()
        target_lang = message.command[1].lower() if cmd == "tercume" else cmd[2:]
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
        try:
            res = requests.get(url).json()
            await message.reply_text(f"🌍 **Tərcümə ({target_lang.upper()}):**\n\n`{res[0][0][0]}`")
        except: await message.reply_text("❌ Xəta.")

    # --- 📄 PDF SİSTEMİ ---
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
            c.setFont("Helvetica", 14)
            c.drawString(70, 320 if photo_path else 800, f"Mezmun: {text_content[:150]}")
        c.save()
        await message.reply_document(pdf_name, caption="📄 PDF hazırdır!"); os.remove(pdf_name)

    # --- 💖 ƏYLƏNCƏ: LOVE (TAM) ---
    @app.on_message(filters.command("love"))
    async def love_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return await message.reply_text("💘 Reply verin və ya ID yazın!")
        u2 = await get_mention(client, target)
        p = int(hashlib.md5(f"{message.from_user.id}{target}".encode()).hexdigest(), 16) % 101
        await message.reply_text(f"💘 {u2} ilə uyğunluq: `{p}%`")

    # --- 🥊 ƏYLƏNCƏ: SLAP (TAM) ---
    @app.on_message(filters.command("slap"))
    async def slap_cmd(client, message):
        if message.reply_to_message:
            await message.reply_text(f"🥊 **{message.reply_to_message.from_user.first_name}** möhkəm şapalaqlandı!")
        else:
            await message.reply_text("🥊 Kimi vurmaq istəyirsən? Reply ver!")

    # --- 🎲 OYUNLAR ---
    @app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
    async def games(client, message):
        em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
        await client.send_dice(message.chat.id, emoji=em[message.command[0]])

    # --- 🛠 ADMİN & SİSTEM ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        ids = list(range(message.reply_to_message.id, message.id))
        for i in range(0, len(ids), 100): await client.delete_messages(message.chat.id, ids[i:i+100])

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message): await message.reply_text(f"🆔 ID: `{message.from_user.id}`\n🆔 Çat: `{message.chat.id}`")

    @app.on_message(filters.command("qr"))
    async def qr_cmd(client, message):
        if len(message.command) < 2: return
        txt = urllib.parse.quote(message.text.split(None, 1)[1])
        await message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}")

    # --- 💰 MƏLUMATLAR ---
    @app.on_message(filters.command("kripto"))
    async def crypto_cmd(client, message):
        try:
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]").json()
            await message.reply_text(f"🪙 BTC: `${float(r[0]['price']):,.2f}`\n💠 ETH: `${float(r[1]['price']):,.2f}`")
        except: pass

    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        if len(message.command) < 2: return
        wikipedia.set_lang("az")
        try: await message.reply_text(f"📖 {wikipedia.summary(message.text.split(None, 1)[1], sentences=2)}")
        except: await message.reply_text("❌ Tapılmadı.")

    @app.on_message(filters.command("proqnoz"))
    async def oracle_cmd(client, message):
        preds = ["Maraqlı hadisə olacaq! ✨", "Bu gün uğurlu keçəcək! 🍀", "💌 Xoş xəbər gələcək!"]
        await message.reply_text(f"🔮 **Kahin:** {random.choice(preds)}")         
