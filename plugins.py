import os, asyncio, requests, urllib.parse, random, hashlib, wikipedia
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType
from gtts import gTTS
from PIL import Image

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

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    TARGET_GROUP = "@sohbetqruprc"

    # --- KOMANDALARIN MENYUSU ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Geniş kömək menyusu"),
            BotCommand("love", "💘 Sevgi testi (Username/ID ilə)"),
            BotCommand("slap", "🥊 Zarafatla şapalaq atar"),
            BotCommand("ses", "🎙 Mətni səsə çevirər"),
            BotCommand("qr", "🖼 QR kod yaradar"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("valyuta", "💰 Günlük məzənnələr"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("tercume", "🌐 Tərcümə (Reply)"),
            BotCommand("etiraf", "🤫 Anonim etiraf"),
            BotCommand("acetiraf", "👤 Adlı etiraf"),
            BotCommand("id", "🆔 ID-ləri göstərər"),
            BotCommand("info", "🎭 İstifadəçi haqqında analiz"),
            BotCommand("purge", "🧹 Mesajları silər"),
            BotCommand("dice", "🎲 Zər atar"),
            BotCommand("slot", "🎰 Slot oyunu"),
            BotCommand("futbol", "⚽ Futbol oyunu"),
            BotCommand("basket", "🏀 Basketbol oyunu")
        ]
        await app.set_bot_commands(commands)

    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await set_commands()
        await message.reply_text("✨ **Bot Full Pro Versiyada Aktivdir!**\n\nBütün komandalar `/` menyusuna əlavə edildi.")

    # --- 1. HELP ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **F U L L  B O T  M E N Y U** 💠\n"
            "╚════════════════════╝\n\n"
            "🖼 **Şəkil Aləti:**\n"
            "🔹 Şəkil göndərin - Bot onu ağ-qara edəcək.\n\n"
            "💖 **Sevgi & Əyləncə:**\n"
            "🔹 `/love [ID/User]` - Sevgi testi.\n"
            "🔹 `/slap` - Reply və ya ID ilə vurun.\n\n"
            "🎙 **Media Alətləri:**\n"
            "🔹 `/ses [mətin]` - Yazını səsə çevirir.\n"
            "🔹 `/qr [link/mətin]` - QR kod yaradır.\n\n"
            "🌍 **Məlumat Bloqu:**\n"
            "🔹 `/wiki [mövzu]` - Vikipediya.\n"
            "🔹 `/valyuta` - Manat kursu.\n"
            "🔹 `/namaz [şəhər]` - Namaz vaxtı.\n"
            "🔹 `/tercume` - Tərcümə (Reply).\n\n"
            "🤫 **Gizli Bölmə:**\n"
            "🔹 `/etiraf` - Anonim etiraf.\n"
            "🔹 `/acetiraf` - Adlı etiraf.\n\n"
            "🛠 **Admin & Digər:**\n"
            "🔹 `/info` - İstifadəçi analizi.\n"
            "🔹 `/purge` - Mesaj silici.\n"
            "🔹 `/id` - ID məlumatları.\n"
            "🔹 `/dice`, `/slot`, `/futbol`, `/basket` - Oyunlar.\n"
        )
        await message.reply_text(help_text)

    # --- 2. 💘 SEVGİ TESTİ (DÜZƏLDİLMİŞ) ---
    @app.on_message(filters.command("love"))
    async def love_test(client, message):
        if len(message.command) < 2 and not message.reply_to_message:
            return await message.reply_text("💘 Kiminlə sevgi testini yoxlamaq istəyirsiniz?")
        
        user1 = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.from_user.id
        user2 = await get_mention(client, target)
        
        combined = f"{message.from_user.id}{target}".encode()
        percentage = int(hashlib.md5(combined).hexdigest(), 16) % 101
        
        if percentage >= 90: decision = "🔥 **Mükəmməl!** Bir-biriniz üçün yaradılmısınız."
        elif percentage >= 70: decision = "❤️ **Çox gözəl!** Aranızda güclü cazibə var."
        elif percentage >= 50: decision = "🧡 **Normal.** Bir az çalışsanız hər şey düzələr."
        elif percentage >= 30: decision = "💛 **Zəif.** Dost qalsanız daha yaxşı olar."
        else: decision = "💔 **Uyğunluq yoxdur.** Başqa qapıya... 😊"
        
        await message.reply_text(f"💘 **Sevgi Testi**\n\n👤 {user1} + {user2}\n📊 **Uyğunluq:** {percentage}%\n📝 **Qərar:** {decision}")

    # --- 3. 🥊 SLAP ---
    @app.on_message(filters.command("slap"))
    async def slap_user(client, message):
        u1 = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        target = message.text.split(None, 1)[1] if len(message.command) > 1 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
        if not target: return await message.reply_text("🥊 Birini 'vurmaq' üçün reply et və ya ID yaz!")
        
        u2 = await get_mention(client, target)
        slaps = [
            f"🥊 {u1}, {u2} şəxsini elə vurdu ki, uşaq hələ də ulduz sayır!",
            f"🥊 {u1}, {u2}-a bir Osmanlı şapalağı daddırdı!",
            f"🥊 {u1} bir kəllə atdı, {u2} ulduzları toplamağa başladı!"
        ]
        await message.reply_text(random.choice(slaps))

    # --- 4. 🤫 ETİRAF SİSTEMİ (STABİL) ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: return await message.reply_text("💬 Etirafınızı yazın.")
        txt = message.text.split(None, 1)[1]
        sender = "Anonim" if message.command[0] == "etiraf" else message.from_user.first_name
        
        check_buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Təsdiqlə", callback_data="acc_et"),
            InlineKeyboardButton("❌ Rədd et", callback_data="rej_et")
        ]])
        
        for o in OWNERS:
            try: await client.send_message(o, f"📩 **Etiraf:**\n`{txt}`\n\n👤 **Kimdən:** {sender}", reply_markup=check_buttons)
            except: continue
        await message.reply_text("✅ Moderatorlara göndərildi.")

    @app.on_callback_query(filters.regex(r"acc_et|rej_et"))
    async def etiraf_callback(client, callback_query):
        msg = callback_query.message.text
        original_text = msg.split("📩 Etiraf:")[1].split("👤 Kimdən:")[0].strip()
        sender_info = msg.split("👤 Kimdən:")[1].strip()

        if callback_query.data == "acc_et":
            await callback_query.answer("Təsdiqləndi və qrupa göndərildi!", show_alert=True)
            await client.send_message(TARGET_GROUP, f"🤫 **Yeni Etiraf:**\n\n`{original_text}`\n\n👤 **Göndərən:** {sender_info}")
            await callback_query.edit_message_text(f"{msg}\n\n✅ **TƏSDİQLƏNDİ**")
        else:
            await callback_query.answer("Rədd edildi.", show_alert=True)
            await callback_query.edit_message_text(f"{msg}\n\n❌ **RƏDD EDİLDİ**")

    # --- 5. 🖼 ŞƏKİL REDAKTORU ---
    @app.on_message(filters.photo)
    async def bw_photo(client, message):
        p_msg = await message.reply_text("⏳ Şəkil ağ-qara edilir...")
        path = await message.download()
        with Image.open(path) as img:
            img.convert("L").save("bw.jpg")
        await message.reply_photo("bw.jpg", caption="🖼 Şəkil ağ-qara edildi.")
        os.remove(path); os.remove("bw.jpg"); await p_msg.delete()

    # --- 6. 🌍 WIKI & SES & QR & VALYUTA ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2: return await message.reply_text("🔍 Mövzu yazın.")
        try:
            wikipedia.set_lang("az")
            summary = wikipedia.summary(message.text.split(None, 1)[1], sentences=3)
            await message.reply_text(f"📖 **Məlumat:**\n\n{summary}")
        except: await message.reply_text("❌ Tapılmadı.")

    @app.on_message(filters.command("ses"))
    async def text_to_speech(client, message):
        if len(message.command) < 2: return
        gTTS(message.text.split(None, 1)[1], lang='az').save("v.mp3")
        await client.send_voice(message.chat.id, "v.mp3")
        os.remove("v.mp3")

    @app.on_message(filters.command("qr"))
    async def make_qr(client, message):
        if len(message.command) < 2: return
        data = urllib.parse.quote(message.text.split(None, 1)[1])
        await client.send_photo(message.chat.id, f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={data}")

    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 **AZN:**\n🇺🇸 USD: `{1/r['rates']['USD']:.2f}`\n🇹🇷 TRY: `{1/r['rates']['TRY']:.2f}`")

    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3").json()
        t = r['data']['timings']
        await message.reply_text(f"🕋 **{city}**: Sübh: `{t['Fajr']}`, Zöhr: `{t['Dhuhr']}`, Axşam: `{t['Maghrib']}`")

    # --- 7. ADMİN & OYUNLAR ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        ids = list(range(message.reply_to_message.id, message.id))
        for i in range(0, len(ids), 100): await client.delete_messages(message.chat.id, ids[i:i+100])

    @app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
    async def games_func(client, message):
        em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
        await client.send_dice(message.chat.id, emoji=em[message.command[0]])

    @app.on_message(filters.command("id"))
    async def id_cmd(client, message):
        await message.reply_text(f"🆔 Sizin ID: `{message.from_user.id}`\n🆔 Çat ID: `{message.chat.id}`")
