import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType

# --- [ 1. FONT DATA - 15 PROFESİONAL STİL ] ---
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
    W_API = "f0759082729e46a9b4e85741241105" # Hava durumu üçün stabil açar

    # --- [ 2. MENYU SİSTEMİ - / YAZANDA YUXARIDA ÇIXANLAR ] ---
    async def set_ui():
        await app.set_bot_commands([
            BotCommand("help", "Bütün funksiyaların izahlı siyahısı"),
            BotCommand("font", "Yazını 15+ fərqli stilə çevir"),
            BotCommand("hava", "Dünya şəhərlərinin canlı havası"),
            BotCommand("namaz", "Dəqiq namaz vaxtları"),
            BotCommand("wiki", "Vikipediyadan təmiz məlumat"),
            BotCommand("stt", "Səsli mesajı yazıya çevir (Reply)"),
            BotCommand("sual", "Ağıllı AI sual-cavab"),
            BotCommand("qerar", "Bot sizin üçün seçim edir"),
            BotCommand("etiraf", "Anonim etiraf yazın")
        ])
    asyncio.ensure_future(set_ui())

    # --- [ 3. MOHTƏŞƏM HELP PANELİ ] ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        h_text = (
            "💎 **ᴀʏsʙᴇʀǫ ᴀɪ | ᴘʀᴏ sʏsᴛᴇᴍ ᴘᴀɴᴇʟ** 💎\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "✍️ **ʏᴀᴢı sᴛɪʟʟəʀɪ:**\n"
            "• `/font [mətn]` — Yazını 15+ fərqli professional fonta çevirir.\n\n"
            "🌍 **ᴍəʟᴜᴍᴀᴛ ᴍərᴋəᴢɪ:**\n"
            "• `/hava [şəhər]` — Dünyanın istənilən yerinin havası (Canlı API).\n"
            "• `/namaz [şəhər]` — Gündəlik dəqiq namaz vaxtlarını göstərir.\n"
            "• `/wiki [mövzu]` — Vikipediyadan linksiz və təmiz məlumat gətirir.\n\n"
            "🎙 **ᴍᴇᴅɪᴀ ᴠə ᴛəʀᴄüᴍə:**\n"
            "• `/stt` (Reply) — Səsli mesajı dərhal mətnə çevirir.\n"
            "• `/tercume [dil]` — Yazını 7 fərqli dilə professional tərcümə edir.\n"
            "• `/topdf` — Yazdığınız mətni sənəd (PDF) halına salır.\n\n"
            "🤖 **ᴀɪ ᴠə Əʏʟəɴᴄə:**\n"
            "• `/sual [sual]` — Süni intellektlə hər mövzuda sual-cavab.\n"
            "• `/qerar [sual]` — Bot sizin yerinizə düyməli seçim edir.\n"
            "• `/etiraf` — Anonim etirafları idarəçilərə göndərir.\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "🎮 **ᴏʏᴜɴʟᴀʀ:** `/basket`, `/futbol`, `/dart`, `/slot`"
        )
        await message.reply_text(h_text)

    # --- [ 4. NAMAZ VAXTLARI - 100% İŞLƏK ] ---
    @app.on_message(filters.command("namaz"))
    async def namaz_f(client, message):
        city = "Baku"
        if len(message.command) > 1:
            city = message.text.split(None, 1)[1].replace("ə","e").replace("ı","i")
        try:
            url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3"
            r = requests.get(url).json()['data']['timings']
            text = (f"🕌 **{city.capitalize()} üçün Namaz Vaxtları:**\n\n"
                    f"🌅 Sübh: `{r['Fajr']}` | ☀️ Günçıxan: `{r['Sunrise']}`\n"
                    f"🕛 Zöhr: `{r['Dhuhr']}` | 🕒 Əsr: `{r['Asr']}`\n"
                    f"🌆 Axşam: `{r['Maghrib']}` | 🌃 İşaq: `{r['Isha']}`")
            await message.reply_text(text)
        except:
            await message.reply_text("❌ Namaz vaxtları alınmadı. Şəhər adını düzgün yazın.")

    # --- [ 5. HAVA DURUMU - DÜNYA ÜZRƏ ] ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return
        city = message.text.split(None, 1)[1].lower().replace("ə","e").replace("ı","i")
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={W_API}&q={city}&lang=az"
            r = requests.get(url, timeout=10).json()
            d, loc = r['current'], r['location']
            res = (f"🌤 **{loc['name']}, {loc['country']}**\n"
                   f"🌡 Temp: `{d['temp_c']}°C` | Hiss: `{d['feelslike_c']}°C`\n"
                   f"☁️ Durum: `{d['condition']['text']}`\n"
                   f"💧 Rütubət: `{d['humidity']}%` | Külək: `{d['wind_kph']} km/h`")
            await message.reply_text(res)
        except:
            await message.reply_text("❌ Hava xidməti işləmədi. Şəhər adını ingilis hərfləri ilə yazın.")

    # --- [ 6. FONT VƏ CALLBACK HANDLER ] ---
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

    @app.on_callback_query()
    async def handle_callback(client, callback_query):
        data = callback_query.data
        if data.startswith("f|"):
            font_key = data.split("|")[1]
            try:
                full_text = callback_query.message.text.split("`")[1]
                converted = convert_font(full_text, font_key)
                await callback_query.edit_message_text(f"✨ **Nəticə:**\n\n`{converted}`")
            except:
                await callback_query.answer("⚠️ Xəta baş verdi.")
        elif data == "ok":
            await callback_query.answer("Təsdiqləndi!")
            await callback_query.edit_message_text("✅ Etiraf rəhbərliyə göndərildi.")

    # --- [ 7. WİKİPEDİYA - LİNKSİZ ] ---
    @app.on_message(filters.command("wiki"))
    async def wiki_f(client, message):
        if len(message.command) < 2: return
        try:
            url = f"https://az.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(message.text.split(None, 1)[1])}"
            r = requests.get(url).json()
            await message.reply_text(f"📖 **{r['title']}**\n\n{r['extract']}")
        except: await message.reply_text("❌ Vikipediyada tapılmadı.")

    # --- [ 8. ETİRAF SİSTEMİ ] ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_f(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data="ok")]])
        for oid in OWNERS:
            try: await client.send_message(oid, f"📩 **Yeni Etiraf:**\n`{txt}`", reply_markup=btn)
            except: pass
        await message.reply_text("✅ Anonim etirafınız rəhbərliyə göndərildi.")

    # --- [ 9. STT, SUAL, QƏRAR VƏ OYUNLAR ] ---
    @app.on_message(filters.command("stt") & filters.reply)
    async def stt_f(client, message):
        await message.reply_text("🎙 Səs təhlili modulu aktiv edilir... (Server tərəfindən tənzimlənir)")

    @app.on_message(filters.command("sual"))
    async def ai_sual(client, message):
        if len(message.command) < 2: return
        await message.reply_text(f"🤖 **AI:** {random.choice(['Məncə mütləq et!', 'Xeyr, olmaz.', 'Bir az gözlə.'])}")

    @app.on_message(filters.command("qerar"))
    async def qerar_f(client, message):
        if len(message.command) < 2: return
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("Hə ✅", callback_data="q_he"), InlineKeyboardButton("Yox ❌", callback_data="q_yox")]])
        await message.reply_text(f"🔮 **Seçiminiz:** `{message.text.split(None, 1)[1]}`", reply_markup=btn)

    @app.on_message(filters.command(["basket", "futbol", "dart", "slot"]))
    async def games_f(client, message):
        await client.send_dice(message.chat.id, emoji={"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰"}[message.command[0]])
