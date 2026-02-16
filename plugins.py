import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from gtts import gTTS
from PIL import Image

# --- YARDIMÇI FUNKSİYA: ADMİN YOXLAMA ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- MENTION YARADICI ---
async def get_mention(client, user_input):
    try:
        user = await client.get_users(user_input)
        return f"[{user.first_name}](tg://user?id={user.id})"
    except:
        return f"`{user_input}`"

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]

    # --- KOMANDALARIN MENYUSU (/ yazanda mesajın üstündə çıxanlar) ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Geniş kömək menyusu"),
            BotCommand("love", "💘 Sevgi testi (ID/User/Reply)"),
            BotCommand("slap", "🥊 Şapalaq atar (ID/User/Reply)"),
            BotCommand("ses", "🎙 Mətni səsə çevirər"),
            BotCommand("qr", "🖼 QR kod yaradar"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("valyuta", "💰 Günlük məzənnələr"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("tercume", "🌐 Tərcümə (Reply)"),
            BotCommand("etiraf", "🤫 Anonim etiraf"),
            BotCommand("acetiraf", "👤 Adlı etiraf"),
            BotCommand("info", "🎭 İstifadəçi analizi"),
            BotCommand("id", "🆔 ID məlumatları"),
            BotCommand("purge", "🧹 Mesajları təmizlə"),
            BotCommand("dice", "🎲 Zər at"),
            BotCommand("slot", "🎰 Slot oyunu"),
            BotCommand("futbol", "⚽ Futbol oyunu"),
            BotCommand("basket", "🏀 Basketbol oyunu")
        ]
        await app.set_bot_commands(commands)

    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await set_commands()
        await message.reply_text("✨ **Bot Bütün Funksiyaları İlə Aktivdir!**\n\nBütün komandalar menyuya əlavə edildi.")

    # --- 1. HELP ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **F U L L  B O T  M E N Y U** 💠\n"
            "╚════════════════════╝\n\n"
            "🖼 **Şəkil Redaktoru:**\n"
            "🔹 Bot şəkil göndərin - Avtomatik ağ-qara edər.\n\n"
            "💖 **Sevgi & Əyləncə:**\n"
            "🔹 `/love [ID/User]` - Sevgi uyğunluğu.\n"
            "🔹 `/slap [ID/User]` - Zarafatla şapalaq atar.\n"
            "🔹 `/dice`, `/slot`, `/futbol`, `/basket` - Oyunlar.\n\n"
            "🎙 **Media Alətləri:**\n"
            "🔹 `/ses [mətin]` - Yazını səsə çevirir.\n"
            "🔹 `/qr [mətin]` - QR kod yaradar.\n\n"
            "🌍 **Məlumat Bloqu:**\n"
            "🔹 `/wiki [mövzu]` - Vikipediyada axtarış.\n"
            "🔹 `/valyuta` - Günlük Manat kursu.\n"
            "🔹 `/namaz [şəhər]` - Namaz vaxtları.\n"
            "🔹 `/tercume` - Tərcümə (Reply).\n\n"
            "🤫 **Gizli Bölmə:**\n"
            "🔹 `/etiraf` / `/acetiraf` - Etiraf sistemi.\n\n"
            "🛠 **Admin & Sistem:**\n"
            "🔹 `/id` - ID məlumatları.\n"
            "🔹 `/info` - User analizi.\n"
            "🔹 `/purge` - Mesaj silici.\n"
        )
        await message.reply_text(help_text)

    # --- 2. 💘 SEVGİ TESTİ (ANCAQ SEVGİ MESAJLARI) ---
    @app.on_message(filters.command("love"))
    async def love_test(client, message):
        if len(message.command) < 2 and not message.reply_to_message:
            return await message.reply_text("💘 Kiminlə yoxlayım? ID, Username yaz və ya Reply et.")
        
        user1_m = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.from_user.id
        user2_m = await get_mention(client, target)
        
        combined = f"{message.from_user.id}{target}".encode()
        p = int(hashlib.md5(combined).hexdigest(), 16) % 101
        
        # Ancaq sevgi qərarları
        if p > 80: d = "💖 Toy nə vaxtdır? Ba belə!"
        elif p > 50: d = "🧡 Uyğunluq var, pis deyil."
        else: d = "💔 Ayrılın, xeyir yoxdur..."
        
        await message.reply_text(f"💘 **Sevgi Testi**\n\n👤 {user1_m} + {user2_m}\n📊 **Uyğunluq:** {p}%\n📝 **Qərar:** {d}")

    # --- 3. 🥊 SLAP (ANCAQ ŞAPALAQ MESAJLARI) ---
    @app.on_message(filters.command("slap"))
    async def slap_user(client, message):
        if len(message.command) < 2 and not message.reply_to_message:
            return await message.reply_text("🥊 Vurmaq üçün birini reply et və ya ID/User yaz.")
        
        u1_m = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.from_user.id
        u2_m = await get_mention(client, target)
        
        # Ancaq şapalaq mesajları
        slaps = [
            f"🥊 {u1_m}, {u2_m} şəxsini elə vurdu ki, hələ də ulduz sayır!",
            f"🥊 {u1_m} {u2_m}-a bir Osmanlı şapalağı daddırdı!",
            f"🥊 {u1_m}, {u2_m} şəxsini qatlayıb qoydu cibinə!"
        ]
        await message.reply_text(random.choice(slaps))

    # --- 4. 🤫 ETİRAF SİSTEMİ (DÜZƏLDİLMİŞ) ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        sender = "Anonim" if message.command[0] == "etiraf" else message.from_user.first_name
        
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Təsdiqlə", callback_data="acc_et"),
            InlineKeyboardButton("❌ Rədd et", callback_data="rej_et")
        ]])
        
        for o in OWNERS:
            try: await client.send_message(o, f"📩 **Etiraf:** {txt}\n👤 **Kimdən:** {sender}", reply_markup=btn)
            except: continue
        await message.reply_text("✅ Moderatorlara göndərildi.")

    @app.on_callback_query(filters.regex(r"acc_et|rej_et"))
    async def etiraf_callback(client, callback_query):
        # Donma probleminin həlli buradadır (answer)
        if callback_query.data == "acc_et":
            await callback_query.answer("Təsdiqləndi!", show_alert=True)
            await callback_query.edit_message_text(f"{callback_query.message.text}\n\n✅ **TƏSDİQLƏNDİ**")
        else:
            await callback_query.answer("Rədd edildi!", show_alert=True)
            await callback_query.edit_message_text(f"{callback_query.message.text}\n\n❌ **RƏDD EDİLDİ**")

    # --- 5. 🖼 ŞƏKİL REDAKTORU ---
    @app.on_message(filters.photo)
    async def black_white(client, message):
        p_msg = await message.reply_text("⏳ Şəkil ağ-qara edilir...")
        path = await message.download()
        with Image.open(path) as img:
            img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Şəkil ağ-qara edildi.")
        os.remove(path)
        os.remove("bw.jpg")
        await p_msg.delete()

    # --- 6. 🌍 WIKI, SES, QR, VALYUTA, NAMAZ ---
    @app.on_message(filters.command("wiki"))
    async def wiki_cmd(client, message):
        if len(message.command) < 2: return
        q = message.text.split(None, 1)[1]
        try:
            wikipedia.set_lang("az")
            await message.reply_text(f"📖 **{q}**\n\n{wikipedia.summary(q, sentences=3)}")
        except: await message.reply_text("❌ Tapılmadı.")

    @app.on_message(filters.command("ses"))
    async def ses_cmd(client, message):
        if len(message.command) < 2: return
        t = message.text.split(None, 1)[1]
        gTTS(t, lang='az').save("v.mp3")
        await client.send_voice(message.chat.id, "v.mp3")
        os.remove("v.mp3")

    @app.on_message(filters.command("qr"))
    async def qr_cmd(client, message):
        if len(message.command) < 2: return
        d = message.text.split(None, 1)[1]
        u = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(d)}"
        await client.send_photo(message.chat.id, u)

    @app.on_message(filters.command("valyuta"))
    async def val_cmd(client, message):
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 USD: `{1/r['rates']['USD']:.2f}`\n🇹🇷 TRY: `{1/r['rates']['TRY']:.2f}`")

    @app.on_message(filters.command("namaz"))
    async def nam_cmd(client, message):
        c = message.command[1] if len(message.command) > 1 else "Baku"
        r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={c}&country=Azerbaijan&method=3").json()
        t = r['data']['timings']
        await message.reply_text(f"🕋 {c}: Sübh: {t['Fajr']}, Zöhr: {t['Dhuhr']}, Axşam: {t['Maghrib']}")

    # --- 7. ADMİN & OYUNLAR ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_cmd(client, message):
        if not await check_admin(client, message, OWNERS): return
        if message.reply_to_message:
            ids = list(range(message.reply_to_message.id, message.id))
            for i in range(0, len(ids), 100): await client.delete_messages(message.chat.id, ids[i:i+100])

    @app.on_message(filters.command(["basket", "futbol", "dice", "slot"]))
    async def games_cmd(client, message):
        try: await client.send_dice(message.chat.id, emoji={"basket":"🏀", "futbol":"⚽", "dice":"🎲", "slot":"🎰"}[message.command[0]])
        except: pass

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message):
        await message.reply_text(f"🆔 ID: `{message.from_user.id}`")
