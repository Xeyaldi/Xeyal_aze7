import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- MƏLUMAT BAZASI ---
user_stats = {} 
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

# --- RÜTBƏ TƏYİNİ ---
def get_rank(count):
    if count > 10000: return "💎 Marşal"
    if count > 5000: return "🌟 General"
    if count > 2000: return "🎖️ Polkovnik"
    if count > 1000: return "🎖️ Mayor"
    if count > 500: return "🎗️ Kapitan"
    if count > 200: return "💂 Leytenant"
    if count > 50: return "🔫 Çavuş"
    return "🛡️ Sıravi"

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    TARGET_GROUP = "@sohbetqruprc"

    # --- KOMANDALARIN MENYUSU ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Geniş kömək menyusu"),
            BotCommand("tercume", "🌍 Tərcümə (az/en/ru/tr/de/fr)"),
            BotCommand("topsiralama", "🎖️ Aktivlik Top 20"),
            BotCommand("topkarma", "🎭 Karma Reytinqi"),
            BotCommand("pdf", "📄 Mesajı PDF et (Reply)"),
            BotCommand("kripto", "🪙 Kripto kursları"),
            BotCommand("love", "💘 Sevgi testi"),
            BotCommand("slap", "🥊 Şapalaq"),
            BotCommand("qr", "🖼 QR kod yaradıcı"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("valyuta", "💰 Məzənnələr"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("etiraf", "🤫 Anonim etiraf"),
            BotCommand("id", "🆔 ID-ləri göstərər"),
            BotCommand("purge", "🧹 Mesajları silər")
        ]
        await app.set_bot_commands(commands)

    # --- AVTOMATİK ARXA FON SKANI ---
    async def background_history_scan(client, chat_id):
        if chat_id not in user_stats: user_stats[chat_id] = {}
        try:
            async for msg in client.get_chat_history(chat_id, limit=10000):
                if msg.from_user and not msg.from_user.is_bot:
                    u_id = msg.from_user.id
                    user_stats[chat_id][u_id] = user_stats[chat_id].get(u_id, 0) + 1
        except: pass

    # --- GLOBAL HANDLER ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def global_handler(client, message):
        c_id, u_id = message.chat.id, message.from_user.id
        if c_id not in user_stats:
            user_stats[c_id] = {}
            asyncio.create_task(background_history_scan(client, c_id))
        user_stats[c_id][u_id] = user_stats[c_id].get(u_id, 0) + 1

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

    # --- 🔍 GİZLİ SKAN ---
    @app.on_message(filters.command("skan") & filters.group)
    async def scan_history(client, message):
        if not await check_admin(client, message, OWNERS): return
        m_wait = await message.reply_text("🔍 Mesajlar analiz edilir...")
        asyncio.create_task(background_history_scan(client, message.chat.id))
        await m_wait.edit("✅ Skan başladı.")

    # --- 📚 HELP MENYU ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **B O T  P R O  M E N Y U** 💠\n"
            "╚════════════════════╝\n\n"
            "🎖️ **REYТİNQ:**\n"
            "🔹 `/topsiralama` - Top 20 aktiv üzv.\n"
            "🔹 `/topkarma` - Ən çox hörmət edilənlər.\n\n"
            "🌍 **TƏRCÜMƏ SİSTEMİ:**\n"
            "🔹 Mesaja reply verib istifadə edin:\n"
            "🔹 `/tercume az` və ya `/traz`\n"
            "🔹 `/tercume en` və ya `/tren`\n"
            "🔹 `/tercume ru` və ya `/trru`\n"
            "🔹 `/tercume tr` və ya `/trtr`\n"
            "🔹 `/tercume de` və ya `/trde`\n"
            "🔹 `/tercume fr` və ya `/trfr`\n\n"
            "📄 **MULTİMEDİA:**\n"
            "🔹 `/pdf` - Şəkil/Mətni dərhal PDF edər.\n"
            "🔹 `/qr [mətn]` - QR kod yaradar.\n\n"
            "💰 **MƏLUMAT:**\n"
            "🔹 `/kripto`, `/valyuta`, `/wiki`, `/namaz`.\n\n"
            "💖 **ƏYLƏNCƏ:**\n"
            "🔹 `/love`, `/slap`, `/dice`, `/slot`, `/futbol`.\n\n"
            "🛠 **ADMİN:**\n"
            "🔹 `/purge`, `/id`, `/etiraf`.\n"
        )
        await message.reply_text(help_text)

    # --- 🔤 TƏRCÜMƏ ---
    @app.on_message(filters.command(["tercume", "traz", "tren", "trru", "trtr", "trde", "trfr"]))
    async def multi_translate(client, message):
        if not message.reply_to_message:
            return await message.reply_text("❌ Tərcümə üçün mesaja reply verin!")
        
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text: return

        cmd = message.command[0].lower()
        if cmd == "tercume":
            if len(message.command) < 2:
                return await message.reply_text("💡 Nümunə: `/tercume en` (Mesaja reply verərək)")
            target_lang = message.command[1].lower()
        else:
            target_lang = cmd[2:]

        valid_langs = ["az", "en", "ru", "tr", "de", "fr"]
        if target_lang not in valid_langs:
            return await message.reply_text(f"❌ Dəstəklənən dillər: {', '.join(valid_langs)}")

        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
        try:
            res = requests.get(url).json()
            await message.reply_text(f"🌍 **Tərcümə ({target_lang.upper()}):**\n\n`{res[0][0][0]}`")
        except:
            await message.reply_text("❌ Tərcümə zamanı xəta baş verdi.")

    # --- TOPSİRALAMA ---
    @app.on_message(filters.command("topsiralama") & filters.group)
    async def top_ranks(client, message):
        c_id = message.chat.id
        if c_id not in user_stats or not user_stats[c_id]:
            return await message.reply_text("🪖 Məlumat yoxdur.")
        sorted_users = sorted(user_stats[c_id].items(), key=lambda x: x[1], reverse=True)[:20]
        text = "🎖️ **Qrupun Top 20 Aktiv Üzvü**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, count) in enumerate(sorted_users, 1):
            mention = await get_mention(client, u_id); rank = get_rank(count)
            text += f"{i:02d}. {rank} | {mention}\n╰─ 💬 Mesaj: `{count}`\n\n"
        await message.reply_text(text)

    @app.on_message(filters.command("topkarma") & filters.group)
    async def top_karma_cmd(client, message):
        c_id = message.chat.id
        if c_id not in user_karma or not user_karma[c_id]:
            return await message.reply_text("🎭 Karma hələ yoxdur.")
        sorted_karma = sorted(user_karma[c_id].items(), key=lambda x: x[1], reverse=True)[:10]
        text = "🎭 **Karma Reytinqi (Top 10)**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, val) in enumerate(sorted_karma, 1):
            mention = await get_mention(client, u_id)
            text += f"{i}. {mention} — `{val}` Karma\n"
        await message.reply_text(text)

    @app.on_message(filters.command("pdf"))
    async def instant_pdf(client, message):
        if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
        target = message.reply_to_message
        photo_path = await target.download() if target.photo else None
        text_content = target.caption if target.photo else (target.text if target.text else None)
        wait_msg = await message.reply_text("⏳ PDF hazırlanır...")
        pdf_name = f"pdf_{message.from_user.id}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        if photo_path:
            with Image.open(photo_path) as img: img.convert("L").save(photo_path)
            c.drawImage(photo_path, 50, 350, 500, 450); os.remove(photo_path)
        if text_content:
            c.setFont("Helvetica", 14)
            c.drawString(70, 320 if photo_path else 800, f"Mezmun: {text_content[:150]}")
        c.showPage(); c.save()
        await message.reply_document(pdf_name, caption="📄 Budur, PDF-iniz hazırdır!")
        os.remove(pdf_name); await wait_msg.delete()

    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_handler(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        sender = "Anonim" if message.command[0] == "etiraf" else message.from_user.first_name
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data="acc_et")]])
        for o in OWNERS: await client.send_message(o, f"📩 Etiraf: `{txt}`\n👤 Kimdən: {sender}", reply_markup=btn)
        await message.reply_text("✅ Göndərildi.")

    @app.on_callback_query(filters.regex("acc_et"))
    async def acc_callback(client, callback_query):
        await client.send_message(TARGET_GROUP, f"🤫 **Etiraf:**\n\n{callback_query.message.text}")
        await callback_query.edit_message_text("✅ Təsdiqləndi.")

    @app.on_message(filters.photo)
    async def bw_photo(client, message):
        path = await message.download()
        with Image.open(path) as img: img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Ağ-qara edildi.")
        os.remove(path); os.remove("bw.jpg")

    @app.on_message(filters.command("love"))
    async def love_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target)
        p = int(hashlib.md5(f"{message.from_user.id}{target}".encode()).hexdigest(), 16) % 101
        await message.reply_text(f"💘 {u2} ilə uyğunluq: `{p}%`")

    @app.on_message(filters.command("slap"))
    async def slap_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target)
        await message.reply_text(f"🥊 {u2} şapalaqlandı!")

    @app.on_message(filters.command("kripto"))
    async def crypto_cmd(client, message):
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]").json()
        await message.reply_text(f"🪙 BTC: `${float(r[0]['price']):,.2f}`\n💠 ETH: `${float(r[1]['price']):,.2f}`")

    @app.on_message(filters.command("valyuta"))
    async def val_cmd(client, message):
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 USD/AZN: `{1/r['rates']['USD']:.2f}`")

    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        wikipedia.set_lang("az")
        try: await message.reply_text(f"📖 {wikipedia.summary(message.text.split(None, 1)[1], sentences=2)}")
        except: await message.reply_text("❌ Tapılmadı.")

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

    @app.on_message(filters.command("qr"))
    async def qr_cmd(client, message):
        if len(message.command) < 2: return
        txt = urllib.parse.quote(message.text.split(None, 1)[1])
        await message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}")
