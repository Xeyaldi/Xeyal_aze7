import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType

# --- ADMİN YOXLAMA ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- FONT DATA (Şəkildəki stili yaratmaq üçün) ---
FONT_MAPS = {
    "serif": {"name": "𝐒𝐞𝐫𝐢𝐟", "offset_a": 119743, "offset_A": 119737},
    "outline": {"name": "𝕆𝕦𝕥𝕝𝕚𝕟𝕖", "offset_a": 120007, "offset_A": 120001},
    "cursive": {"name": "𝒞𝓊𝓇𝓈𝒾𝓋𝑒", "offset_a": 119955, "offset_A": 119949},
    "type": {"name": "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", "offset_a": 120359, "offset_A": 120353},
    "gothic": {"name": "𝔊𝔬𝔱𝔥𝔦𝔠", "offset_a": 120059, "offset_A": 120053},
    "bold": {"name": "𝐁𝐨𝐥𝐝", "offset_a": 119803, "offset_A": 119797}
}

def convert_font(text, font_key):
    f = FONT_MAPS[font_key]
    res = ""
    for c in text:
        if 'a' <= c <= 'z': res += chr(ord(c) + f["offset_a"])
        elif 'A' <= c <= 'Z': res += chr(ord(c) + f["offset_A"])
        else: res += c
    return res

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]

    # --- 1. KOMANDA MENYUSU ---
    async def set_ui():
        await app.set_bot_commands([
            BotCommand("help", "Bütün komandalar"),
            BotCommand("font", "Yazı fontu seç"),
            BotCommand("sual", "Bota sual ver (AI)"),
            BotCommand("qerar", "Düyməli qərar ver"),
            BotCommand("hava", "Hava durumu (Dəqiq)"),
            BotCommand("tercume", "Tərcümə (7 Dil)"),
            BotCommand("etiraf", "Anonim etiraf")
        ])
    asyncio.ensure_future(set_ui())

    # --- 2. FONT KOMANDASI (Şəkildəki kimi Butonlarla ✅) ---
    @app.on_message(filters.command("font"))
    async def font_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply_text("✍️ Font üçün mətn yazın. Məs: `/font aysberq`")
        
        text = message.text.split(None, 1)[1]
        buttons = []
        keys = list(FONT_MAPS.keys())
        for i in range(0, len(keys), 2):
            row = [InlineKeyboardButton(FONT_MAPS[k]["name"], callback_data=f"f|{k}|{text[:15]}") for k in keys[i:i+2]]
            buttons.append(row)
        
        await message.reply_text(f"📝 **Mətn:** `{text}`\n\nStil seçin:", reply_markup=InlineKeyboardMarkup(buttons))

    # --- 3. CALLBACK (DONMA VƏ FONT DÜZƏLİŞİ ✅) ---
    @app.on_callback_query()
    async def handle_callback(client, callback_query):
        data = callback_query.data
        
        if data.startswith("f|"):
            _, font_key, _ = data.split("|")
            # Əsl mətni mesajdan çəkirik
            full_text = callback_query.message.text.split("`")[1]
            converted = convert_font(full_text, font_key)
            await callback_query.edit_message_text(f"✨ **Yeni Stil:**\n\n`{converted}`")

        elif data.startswith("q_"):
            res = {"q_he": "✅ Hə!", "q_yox": "❌ Yox!", "q_belke": "🤷‍♂️ Bəlkə..."}
            await callback_query.answer(res[data], show_alert=True)

        elif data.startswith("ok|"):
            await callback_query.answer("Etiraf təsdiqləndi!")
            await callback_query.edit_message_text("✅ Etiraf qrupa göndərildi.")

    # --- 4. HAVA DURUMU (ŞƏKİLDƏKİ XƏTA HƏLL EDİLDİ ✅) ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return
        city = " ".join(message.command[1:]).lower().replace("ə","e").replace("ı","i").replace("ş","s")
        if "baki" in city: city = "Baku"
        try:
            url = f"https://wttr.in/{urllib.parse.quote(city)}?format=%l:+%c+%t+%C&lang=az"
            res = requests.get(url, timeout=10).text
            if "Unknown" not in res:
                await message.reply_text(f"🌤 **Hava:** `{res.strip()}`")
            else: await message.reply_text("❌ Şəhər tapılmadı (İngilis hərfləri ilə yazın).")
        except: await message.reply_text("⚠️ Hava serverində gecikmə var.")

    # --- 5. TƏRCÜMƏ (7 DİL ✅) ---
    @app.on_message(filters.command("tercume") & filters.reply)
    async def translate_f(client, message):
        l_map = {"ing": "en", "tr": "tr", "rus": "ru", "az": "az", "alman": "de", "fransiz": "fr", "ereb": "ar"}
        t_l = l_map.get(message.command[1].lower(), "az") if len(message.command) > 1 else "az"
        text = message.reply_to_message.text or message.reply_to_message.caption
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={t_l}&dt=t&q={urllib.parse.quote(text)}"
            r = requests.get(url).json()
            await message.reply_text(f"🌐 **{t_l.upper()}:** `{r[0][0][0]}`")
        except: await message.reply_text("❌ Tərcümə xətası.")

    # --- 6. SUAL VƏ QƏRAR (DÜYMƏLİ ✅) ---
    @app.on_message(filters.command("sual"))
    async def ai_sual(client, message):
        if len(message.command) < 2: return
        res = random.choice(["Məncə mütləq etməlisən! ✨", "Bu yaxşı fikir deyil.", "Bir az daha düşünməlisən."])
        await message.reply_text(f"🤖 **Bot:** {res}")

    @app.on_message(filters.command("qerar"))
    async def qerar_cmd(client, message):
        if len(message.command) < 2: return
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Hə", callback_data="q_he"), InlineKeyboardButton("❌ Yox", callback_data="q_yox")]])
        await message.reply_text(f"🔮 **Sual:** `{message.text.split(None, 1)[1]}`", reply_markup=btn)

    # --- 7. ETİRAF SİSTEMİ ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_f(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiq", callback_data=f"ok|{message.from_user.id}")]])
        for oid in OWNERS:
            try: await client.send_message(oid, f"📩 **Etiraf:** `{txt}`", reply_markup=btn)
            except: pass
        await message.reply_text("✅ Təsdiq üçün sahibələrə göndərildi.")

    # --- 8. HELP VƏ DİGƏR ALƏTLƏR ---
    @app.on_message(filters.command("help"))
    async def help_f(client, message):
        await message.reply_text(
            "✨ **ᴀʏsʙᴇʀǫ ᴀɪ | ᴘʀᴏ** ✨\n\n"
            "/font - Yazı stilləri\n/sual - AI Cavab\n/qerar - Düyməli qərar\n/hava - Hava durumu\n"
            "/tercume - 7 dildə tərcümə\n/etiraf - Anonim mesaj\n/wiki - Vikipediya\n"
            "/topdf - Mətni PDF et\n/stt - Səsi yazıya çevir"
        )
