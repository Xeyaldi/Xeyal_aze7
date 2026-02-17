import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia, psycopg2
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

    # --- DATABASE QURULUMU (Sıfırlanmaması üçün) ---
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            chat_id BIGINT, user_id BIGINT, msg_count INTEGER DEFAULT 0,
            PRIMARY KEY (chat_id, user_id)
        );
        CREATE TABLE IF NOT EXISTS user_karma (
            chat_id BIGINT, user_id BIGINT, karma_count INTEGER DEFAULT 0,
            PRIMARY KEY (chat_id, user_id)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

    # --- GLOBAL HANDLER (MESAJ SAYĞACI VƏ KARMA) ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def global_handler(client, message):
        c_id, u_id = message.chat.id, message.from_user.id
        conn = get_db_connection(); cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1)
            ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1
        """, (c_id, u_id))

        if message.reply_to_message and message.reply_to_message.from_user:
            target_id = message.reply_to_message.from_user.id
            if target_id != u_id:
                if message.text == "+":
                    cur.execute("INSERT INTO user_karma (chat_id, user_id, karma_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET karma_count = user_karma.karma_count + 1", (c_id, target_id))
                    await message.reply_text(f"➕ **{message.reply_to_message.from_user.first_name}** karması artdı!")
                elif message.text == "-":
                    cur.execute("INSERT INTO user_karma (chat_id, user_id, karma_count) VALUES (%s, %s, -1) ON CONFLICT (chat_id, user_id) DO UPDATE SET karma_count = user_karma.karma_count - 1", (c_id, target_id))
                    await message.reply_text(f"➖ **{message.reply_to_message.from_user.first_name}** karması azaldı!")
        
        conn.commit(); cur.close(); conn.close()

    # --- HELP MENYU ---
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
            "🔹 `/tercume az` və ya `/traz`\n"
            "🔹 `/tercume en` və ya `/tren`...\n\n"
            "📄 **MULTİMEDİA:**\n"
            "🔹 `/pdf` - PDF edər.\n"
            "🔹 `/qr [mətn]` - QR yaradar.\n\n"
            "🛠 **ADMİN:**\n"
            "🔹 `/purge`, `/id`, `/etiraf`.\n"
        )
        await message.reply_text(help_text)

    # --- TƏRCÜMƏ ---
    @app.on_message(filters.command(["tercume", "traz", "tren", "trru", "trtr", "trde", "trfr"]))
    async def multi_translate(client, message):
        if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text: return
        cmd = message.command[0].lower()
        target_lang = cmd[2:] if cmd != "tercume" else (message.command[1].lower() if len(message.command) > 1 else "az")
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
        try:
            res = requests.get(url).json()
            await message.reply_text(f"🌍 **Tərcümə ({target_lang.upper()}):**\n\n`{res[0][0][0]}`")
        except: await message.reply_text("❌ Xəta baş verdi.")

    # --- TOPSİRALAMA ---
    @app.on_message(filters.command("topsiralama") & filters.group)
    async def top_ranks(client, message):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT user_id, msg_count FROM user_stats WHERE chat_id = %s ORDER BY msg_count DESC LIMIT 20", (message.chat.id,))
        rows = cur.fetchall()
        if not rows: return await message.reply_text("🪖 Məlumat yoxdur.")
        text = "🎖️ **Qrupun Top 20 Aktiv Üzvü**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, count) in enumerate(rows, 1):
            mention = await get_mention(client, u_id); rank = get_rank(count)
            text += f"{i:02d}. {rank} | {mention}\n╰─ 💬 Mesaj: `{count}`\n\n"
        await message.reply_text(text); cur.close(); conn.close()

    # --- TOPKARMA ---
    @app.on_message(filters.command("topkarma") & filters.group)
    async def top_karma_cmd(client, message):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT user_id, karma_count FROM user_karma WHERE chat_id = %s ORDER BY karma_count DESC LIMIT 10", (message.chat.id,))
        rows = cur.fetchall()
        if not rows: return await message.reply_text("🎭 Karma hələ yoxdur.")
        text = "🎭 **Karma Reytinqi (Top 10)**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, val) in enumerate(rows, 1):
            mention = await get_mention(client, u_id)
            text += f"{i}. {mention} — `{val}` Karma\n"
        await message.reply_text(text); cur.close(); conn.close()

    # --- PDF ---
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
            c.setFont("Helvetica", 14); c.drawString(70, 320 if photo_path else 800, f"Mezmun: {text_content[:150]}")
        c.showPage(); c.save()
        await message.reply_document(pdf_name, caption="📄 Budur, PDF-iniz hazırdır!")
        os.remove(pdf_name); await wait_msg.delete()

    # --- ETİRAF ---
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

    # --- LOVE ---
    @app.on_message(filters.command("love"))
    async def love_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target)
        p = int(hashlib.md5(f"{message.from_user.id}{target}".encode()).hexdigest(), 16) % 101
        await message.reply_text(f"💘 {u2} ilə uyğunluq: `{p}%`")

    # --- SLAP ---
    @app.on_message(filters.command("slap"))
    async def slap_cmd(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target); await message.reply_text(f"🥊 {u2} şapalaqlandı!")

    # --- KRİPTO ---
    @app.on_message(filters.command("kripto"))
    async def crypto_cmd(client, message):
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]").json()
        await message.reply_text(f"🪙 BTC: `${float(r[0]['price']):,.2f}`\n💠 ETH: `${float(r[1]['price']):,.2f}`")

    # --- VALYUTA ---
    @app.on_message(filters.command("valyuta"))
    async def val_cmd(client, message):
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 USD/AZN: `{1/r['rates']['USD']:.2f}`")

    # --- WİKİ ---
    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        if len(message.command) < 2: return
        wikipedia.set_lang("az")
        try: await message.reply_text(f"📖 {wikipedia.summary(message.text.split(None, 1)[1], sentences=2)}")
        except: await message.reply_text("❌ Tapılmadı.")

    # --- OYUNLAR ---
    @app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
    async def games(client, message):
        em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
        await client.send_dice(message.chat.id, emoji=em[message.command[0]])

    # --- PURGE ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        ids = list(range(message.reply_to_message.id, message.id))
        for i in range(0, len(ids), 100): await client.delete_messages(message.chat.id, ids[i:i+100])

    # --- ID ---
    @app.on_message(filters.command("id"))
    async def id_cmd(client, message):
        await message.reply_text(f"🆔 Sizin ID: `{message.from_user.id}`\n🆔 Çat ID: `{message.chat.id}`")

    # --- QR ---
    @app.on_message(filters.command("qr"))
    async def qr_cmd(client, message):
        if len(message.command) < 2: return
        txt = urllib.parse.quote(message.text.split(None, 1)[1])
        await message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}")
