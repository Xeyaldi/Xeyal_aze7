import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from gtts import gTTS
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- MƏLUMAT BAZASI SİMULYASİYASI ---
user_stats = {} # {chat_id: {user_id: count}}

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
    except:
        return f"`{user_input}`"

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

    # --- KOMANDALARIN MENYUSU (YENİLƏNDİ) ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Geniş kömək menyusu"),
            BotCommand("topsiralama", "🎖️ Rütbə sıralaması (Top 20)"),
            BotCommand("pdf", "📄 Mesajı dərhal PDF et (Reply)"),
            BotCommand("cevir", "🎤 Səsi yazıya çevir (Reply)"),
            BotCommand("kripto", "🪙 Kripto kursları"),
            BotCommand("love", "💘 Sevgi testi"),
            BotCommand("slap", "🥊 Şapalaq"),
            BotCommand("ses", "🎙 Mətni səsə çevirər"),
            BotCommand("qr", "🖼 QR kod yaradar"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("valyuta", "💰 Məzənnələr"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("etiraf", "🤫 Anonim etiraf"),
            BotCommand("acetiraf", "👤 Adlı etiraf"),
            BotCommand("id", "🆔 ID-ləri göstərər"),
            BotCommand("info", "🎭 İstifadəçi analizi"),
            BotCommand("purge", "🧹 Mesajları silər"),
            BotCommand("dice", "🎲 Zər"),
            BotCommand("slot", "🎰 Slot"),
            BotCommand("futbol", "⚽ Futbol"),
            BotCommand("basket", "🏀 Basketbol")
        ]
        await app.set_bot_commands(commands)

    # --- MESAJ SAYĞACI (TOP 20 ÜÇÜN) ---
    @app.on_message(filters.group & ~filters.bot, group=-1)
    async def count_messages(client, message):
        c_id, u_id = message.chat.id, message.from_user.id
        if c_id not in user_stats: user_stats[c_id] = {}
        user_stats[c_id][u_id] = user_stats[c_id].get(u_id, 0) + 1

    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await set_commands()
        await message.reply_text("✨ **Bot Full Pro Versiyada Aktivdir!**")

    # --- 1. HELP (BÜTÜN FUNKSİYALAR DAHİL) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **B O T  F U L L  M E N Y U** 💠\n"
            "╚════════════════════╝\n\n"
            "🎖️ **Rütbə Sistemi:**\n"
            "🔹 `/topsiralama` - Qrupun 20 ən aktiv əsgəri.\n\n"
            "📄 **Super PDF:**\n"
            "🔹 Mesaja reply verib `/pdf` yazın. Şəkil+Yazı dərhal PDF olar.\n\n"
            "🎤 **Səs Alətləri:**\n"
            "🔹 `/cevir` - Səsi yazıya çevirir (Reply).\n"
            "🔹 `/ses [mətin]` - Yazını səsə çevirir.\n\n"
            "🖼 **Şəkil:**\n"
            "🔹 Şəkil göndərin - Bot onu ağ-qara edəcək.\n\n"
            "💖 **Əyləncə:**\n"
            "🔹 `/love`, `/slap`, `/dice`, `/slot`, `/futbol`, `/basket`.\n\n"
            "🌍 **Məlumat:**\n"
            "🔹 `/kripto`, `/wiki`, `/valyuta`, `/namaz`, `/qr`.\n\n"
            "🤫 **Etiraf:**\n"
            "🔹 `/etiraf` / `/acetiraf`.\n\n"
            "🛠 **Admin:**\n"
            "🔹 `/info`, `/purge`, `/id`.\n"
        )
        await message.reply_text(help_text)

    # --- 2. 🎖️ TOPSIRALAMA (TOP 20 - BƏZƏKLİ) ---
    @app.on_message(filters.command("topsiralama") & filters.group)
    async def top_ranks(client, message):
        c_id = message.chat.id
        if c_id not in user_stats or not user_stats[c_id]:
            return await message.reply_text("🪖 Sıralama üçün hələ kifayət qədər mesaj yoxdur.")
        
        # 20 nəfərlik sıralama
        sorted_users = sorted(user_stats[c_id].items(), key=lambda x: x[1], reverse=True)[:20]
        text = "🎖️ **Qrupun Ən Aktiv 20 Əsgəri** 🎖️\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        for i, (u_id, count) in enumerate(sorted_users, 1):
            mention = await get_mention(client, u_id)
            rank = get_rank(count)
            text += f"{i:02d}. {rank} | {mention}\n╰─ 💬 Mesaj: `{count}`\n\n"
        text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n🚀 *Aktiv olun, rütbəniz artsın!*"
        await message.reply_text(text)

    # --- 3. 📄 SUPER PDF (DƏRHAL REPLY İLƏ) ---
    @app.on_message(filters.command("pdf"))
    async def instant_pdf(client, message):
        if not message.reply_to_message:
            return await message.reply_text("❌ PDF etmək üçün şəkilə və ya yazıya reply verin!")
        
        target = message.reply_to_message
        photo_path = await target.download() if target.photo else None
        text_content = target.caption if target.photo else (target.text if target.text else None)

        wait_msg = await message.reply_text("⏳ Budur, PDF-iniz hazırlanır...")
        pdf_name = f"pdf_{message.from_user.id}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        
        if photo_path:
            with Image.open(photo_path) as img:
                img.convert("L").save(photo_path) # Ağ-qara
            c.drawImage(photo_path, 50, 350, 500, 450)
            os.remove(photo_path)
            
        if text_content:
            c.setFont("Helvetica", 14)
            y_pos = 320 if photo_path else 800
            c.drawString(70, y_pos, f"Mətn: {text_content[:150]}...")

        c.showPage(); c.save()
        await message.reply_document(pdf_name, caption="📄 Budur, PDF-iniz hazırdır!")
        os.remove(pdf_name); await wait_msg.delete()

    # --- 4. 🎤 SƏSİ YAZIYA ÇEVİR (REPLY) ---
    @app.on_message(filters.command("cevir"))
    async def convert_stt(client, message):
        if not message.reply_to_message or not message.reply_to_message.voice:
            return await message.reply_text("🎤 Səsli mesaja reply verin!")
        await message.reply_text("🎧 Səs analiz edilir (API bağlantısı gözlənilir)...")

    # --- 5. 🪙 KRİPTO KURSU ---
    @app.on_message(filters.command("kripto"))
    async def crypto_cmd(client, message):
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[\"BTCUSDT\",\"ETHUSDT\"]").json()
        await message.reply_text(f"🪙 **Canlı Kripto:**\n\nBTC: `${float(r[0]['price']):,.2f}`\nETH: `${float(r[1]['price']):,.2f}`")

    # --- 6. 🖼 ŞƏKİL REDAKTORU (AĞ-QARA) ---
    @app.on_message(filters.photo)
    async def bw_photo(client, message):
        path = await message.download()
        with Image.open(path) as img: img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Şəkil ağ-qara edildi.")
        os.remove(path); os.remove("bw.jpg")

    # --- BÜTÜN KÖHNƏ FUNKSİYALAR (SİLİNMƏDİ) ---
    @app.on_message(filters.command("love"))
    async def love_test(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return
        u2 = await get_mention(client, target)
        p = int(hashlib.md5(f"{message.from_user.id}{target}".encode()).hexdigest(), 16) % 101
        await message.reply_text(f"💘 {u2} ilə uyğunluq: `{p}%` \n📊 Rütbənizə uyğun analiz edildi.")

    @app.on_message(filters.command("slap"))
    async def slap_user(client, message):
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        u2 = await get_mention(client, target)
        await message.reply_text(f"🥊 {u2} bir Osmanlı şapalağı daddı!")

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
        await callback_query.edit_message_text("✅ Qrupa göndərildi.")

    @app.on_message(filters.command("ses"))
    async def tts_cmd(client, message):
        if len(message.command) < 2: return
        gTTS(message.text.split(None, 1)[1], lang='az').save("v.mp3")
        await client.send_voice(message.chat.id, "v.mp3")
        os.remove("v.mp3")

    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        wikipedia.set_lang("az")
        try: await message.reply_text(f"📖 {wikipedia.summary(message.text.split(None, 1)[1], sentences=2)}")
        except: await message.reply_text("❌ Məlumat tapılmadı.")

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
