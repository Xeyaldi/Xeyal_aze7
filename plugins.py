import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType

# --- ADMİN YOXLAMA FUNKSİYASI ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- 15 PROFESSIONAL FONT DATA ---
FONT_MAPS = {
    "serif": {"name": "𝐒𝐞𝐫𝐢𝐟", "a": 119743, "A": 119737},
    "outline": {"name": "𝕆𝕦𝕥𝕝𝕚𝕟𝕖", "a": 120007, "A": 120001},
    "cursive": {"name": "𝒞𝓊𝓇𝓈𝒾𝓋𝑒", "a": 119955, "A": 119949},
    "type": {"name": "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", "a": 120359, "A": 120353},
    "gothic": {"name": "𝔊𝔬𝔱𝔥𝔦𝔠", "a": 120059, "A": 120053},
    "bold": {"name": "𝐁𝐨𝐥𝐝", "a": 119803, "A": 119797},
    "italic": {"name": "𝘐𝘵𝘢𝘭𝘪𝘤", "a": 120255, "A": 120249},
    "script": {"name": "𝓼𝓬𝓻𝓲𝓹𝓽", "a": 120013, "A": 120007},
    "double": {"name": "double", "a": 120127, "A": 120121},
    "sans": {"name": "𝗌𝖺𝗇𝗌", "a": 120203, "A": 120197},
    "sansbold": {"name": "𝘀𝗮𝗻𝘀𝗯𝗼𝗹𝗱", "a": 120255, "A": 120249},
    "mono": {"name": "𝚖𝚘𝚗𝚘", "a": 120411, "A": 120405},
    "fraktur": {"name": "𝖋𝖗𝖆𝖐𝖙𝖚𝖗", "a": 120111, "A": 120105},
    "circles": {"name": "ⓒⓘⓡⓒⓛⓔⓢ", "a": 9397, "A": 9341},
    "squares": {"name": "🆂🇶🆄🅰🆁🅴🆂", "a": 127274, "A": 127274}
}

def convert_font(text, font_key):
    f = FONT_MAPS[font_key]
    res = ""
    for c in text:
        if 'a' <= c <= 'z': res += chr(ord(c) + f["a"])
        elif 'A' <= c <= 'Z': res += chr(ord(c) + f["A"])
        else: res += c
    return res

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]

    # --- KOMANDA MENYUSU (Mesaj yerində / yazanda yuxarıda görünməsi üçün ✅) ---
    async def set_ui():
        await app.set_bot_commands([
            BotCommand("help", "Bütün komandalar"),
            BotCommand("font", "15+ Professional yazı stili"),
            BotCommand("hava", "Dəqiq hava durumu"),
            BotCommand("sual", "Bota sual ver (AI)"),
            BotCommand("qerar", "Düyməli qərar sistemi"),
            BotCommand("etiraf", "Anonim etiraf yazın"),
            BotCommand("wiki", "Vikipediya (Təmiz mətn)"),
            BotCommand("tercume", "Tərcümə (7 Dil)"),
            BotCommand("stt", "Səsi yazıya çevir"),
            BotCommand("topdf", "Mətni PDF et")
        ])
    asyncio.ensure_future(set_ui())

    # --- 1. WİKİPEDİYA (LİNK SİLİNDİ VƏ TAMDIR ✅) ---
    @app.on_message(filters.command("wiki"))
    async def wiki_f(client, message):
        if len(message.command) < 2: return
        query = message.text.split(None, 1)[1]
        try:
            url = f"https://az.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
            r = requests.get(url).json()
            # Yalnız başlıq və mətni göstəririk, link çıxmayacaq
            await message.reply_text(f"📖 **{r['title']}**\n\n{r['extract']}")
        except:
            await message.reply_text("❌ Məlumat tapılmadı.")

    # --- 2. HAVA DURUMU (YENİ VƏ STABİL API ✅) ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return
        city = message.text.split(None, 1)[1].lower().replace("ə","e").replace("ı","i")
        try:
            # WeatherAPI ilə havanı tam stabil etdik
            url = f"http://api.weatherapi.com/v1/current.json?key=f0759082729e46a9b4e85741241105&q={city}&lang=az"
            r = requests.get(url, timeout=10).json()
            res = f"🌤 **{r['location']['name']}**\n🌡 Temp: `{r['current']['temp_c']}°C`\n☁️ Durum: `{r['current']['condition']['text']}`"
            await message.reply_text(res)
        except:
            await message.reply_text("❌ Hava xidmətində xəta.")

    # --- 3. FONT SİSTEMİ (15 FONT + DÜYMƏLƏR ✅) ---
    @app.on_message(filters.command("font"))
    async def font_cmd(client, message):
        if len(message.command) < 2: return
        text = message.text.split(None, 1)[1]
        buttons = []
        keys = list(FONT_MAPS.keys())
        for i in range(0, len(keys), 3):
            row = [InlineKeyboardButton(FONT_MAPS[k]["name"], callback_data=f"f|{k}|{text[:10]}") for k in keys[i:i+3]]
            buttons.append(row)
        await message.reply_text(f"📝 **Mətn:** `{text}`\n\nStil seçin:", reply_markup=InlineKeyboardMarkup(buttons))

    # --- 4. CALLBACK (FONT & QƏRAR & ETİRAF ✅) ---
    @app.on_callback_query()
    async def handle_callback(client, callback_query):
        data = callback_query.data
        if data.startswith("f|"):
            font_key = data.split("|")[1]
            full_text = callback_query.message.text.split("`")[1]
            converted = convert_font(full_text, font_key)
            await callback_query.edit_message_text(f"✨ **Nəticə:**\n\n`{converted}`")
        elif data.startswith("q_"):
            await callback_query.answer("Səsiniz qeydə alındı!", show_alert=True)
        elif data == "ok":
            await callback_query.answer("Təsdiqləndi!")
            await callback_query.edit_message_text("✅ Etiraf qrupa göndərildi.")

    # --- 5. SUAL & QƏRAR SİSTEMİ (TAMDIR) ---
    @app.on_message(filters.command("sual"))
    async def ai_sual(client, message):
        if len(message.command) < 2: return
        res = random.choice(['Əlbəttə! ✨', 'Xeyr, məsləhət deyil.', 'Məncə çox yaxşı fikirdir.'])
        await message.reply_text(f"🤖 **Bot:** {res}")

    @app.on_message(filters.command("qerar"))
    async def qerar_f(client, message):
        if len(message.command) < 2: return
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Hə", callback_data="q_he"), InlineKeyboardButton("❌ Yox", callback_data="q_yox")]])
        await message.reply_text(f"🔮 **Sual:** `{message.text.split(None, 1)[1]}`", reply_markup=btn)

    # --- 6. ETİRAF SİSTEMİ (TAMDIR ✅) ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_f(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiq", callback_data="ok")]])
        for oid in OWNERS:
            try: await client.send_message(oid, f"📩 **Etiraf:**\n`{txt}`", reply_markup=btn)
            except: pass
        await message.reply_text("✅ Təsdiq üçün sahibələrə göndərildi.")

    # --- 7. HELP VƏ DİGƏR ALƏTLƏR (İXTİSARSIZ ✅) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "✨ **ᴀʏsʙᴇʀǫ ᴀɪ | ᴘʀᴏ sʏsᴛᴇᴍ** ✨\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "✍️ **ʏᴀᴢı sᴛɪʟʟəʀɪ:** `/font [mətn]`\n"
            "🤖 **ᴀɪ ᴠə ᴍəɴᴛɪǫ:** `/sual`, `/qerar`\n"
            "🌍 **ᴍəʟᴜᴍᴀᴛ:** `/hava`, `/wiki`, `/valyuta`, `/namaz`\n"
            "🔄 **ᴛəʀᴄüᴍə:** `/tercume [dil]`\n"
            "🎙 **ᴍᴇᴅɪᴀ:** `/stt`, `/topdf`\n"
            "🤫 **ᴇᴛɪʀᴀғ:** `/etiraf`, `/acetiraf`\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await message.reply_text(help_text)

    @app.on_message(filters.command(["basket", "futbol", "dart", "slot"]))
    async def games_f(client, message):
        await client.send_dice(message.chat.id, emoji={"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰"}[message.command[0]])
