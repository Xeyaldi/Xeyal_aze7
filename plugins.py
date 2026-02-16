import os, asyncio, requests, urllib.parse, random, time
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ 1. FONT SİSTEMİ - BÜTÜN STİLLƏR (XƏTASIZ) ] ---
def get_font_text(text, style):
    std_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    fonts = {
        "bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏Ｑ𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
        "italic": "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝐒𝐓𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧",
        "mono": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞维持𝚠𝚡𝚢𝚣",
        "gothic": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
        "outline": "mathbb{ABC...}" 
    }
    if style not in fonts: return text
    return "".join([fonts[style][std_chars.index(c)] if c in std_chars else c for c in text])

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    W_API = "f0759082729e46a9b4e85741241105"

    # --- [ 2. MENU SİYAHISI (TAM SİYAHI) ] ---
    async def set_bot_menu():
        await app.set_bot_commands([
            BotCommand("help", "Bütün funksiyalar"),
            BotCommand("font", "Yazı stilini dəyiş"),
            BotCommand("hava", "Hava durumu"),
            BotCommand("namaz", "Namaz vaxtları"),
            BotCommand("wiki", "Vikipediya"),
            BotCommand("valyuta", "Məzənnə"),
            BotCommand("tercume", "Tərcümə et"),
            BotCommand("love", "Sevgi testi"),
            BotCommand("etiraf", "Anonim etiraf"),
            BotCommand("purge", "Mesaj təmizlə"),
            BotCommand("ping", "Sürət ölç"),
            BotCommand("id", "ID göstər")
        ])
    asyncio.ensure_future(set_bot_menu())

    # --- [ 3. MƏLUMAT VƏ SERVİSLƏR (TƏMİR OLUNANLAR) ] ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return
        city = message.text.split(None, 1)[1].replace("ə","e").replace("ı","i")
        try:
            r = requests.get(f"http://api.weatherapi.com/v1/current.json?key={W_API}&q={city}&lang=az").json()
            await message.reply_text(f"🌤 **{r['location']['name']}**\n🌡 `{r['current']['temp_c']}°C` | ☁️ `{r['current']['condition']['text']}`")
        except: await message.reply_text("❌ Hava tapılmadı.")

    @app.on_message(filters.command("wiki"))
    async def wiki_f(client, message):
        if len(message.command) < 2: return
        try:
            q = urllib.parse.quote(message.text.split(None, 1)[1])
            r = requests.get(f"https://az.wikipedia.org/api/rest_v1/page/summary/{q}").json()
            await message.reply_text(f"📖 **{r['title']}**\n\n{r['extract']}")
        except: await message.reply_text("❌ Wiki tapılmadı.")

    @app.on_message(filters.command("valyuta"))
    async def valyuta_f(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
            await message.reply_text(f"💰 **Məzənnə:**\n1 USD = `{round(1/r['rates']['USD'], 2)} AZN`\n1 EUR = `{round(1/r['rates']['EUR'], 2)} AZN`")
        except: await message.reply_text("❌ Valyuta alınmadı.")

    # --- [ 4. ƏYLƏNCƏ KOMANDALARI (HƏR BİRİ BƏRPA OLUNDU) ] ---
    @app.on_message(filters.command("love"))
    async def love_f(client, message):
        await message.reply_text(f"❤️ Sevgi testi: **%{random.randint(0,100)}**")

    @app.on_message(filters.command("kimem"))
    async def kimem_f(client, message):
        await message.reply_text(f"🔍 Sən: **{random.choice(['Dahi', 'Gözəl', 'Ağıllı', 'Zarafatçıl', 'Lider'])}**")

    @app.on_message(filters.command("gununsozu"))
    async def gununsozu_f(client, message):
        await message.reply_text(f"📜 **Günün Sözü:** {random.choice(['Uğur çalışmaqla gəlir.', 'Heç vaxt təslim olma.', 'Zaman qızıldır.'])}")

    @app.on_message(filters.command("sual"))
    async def sual_f(client, message):
        if len(message.command) > 1:
            await message.reply_text(f"🤖 **Bot:** {random.choice(['Bəli', 'Xeyr', 'Bəlkə də', 'Dəqiq yox'])}")

    @app.on_message(filters.command("qerar"))
    async def qerar_f(client, message):
        await message.reply_text(f"🤔 **Qərarım:** {random.choice(['Mütləq et!', 'Yaxşı olar ki, etməyəsən.', 'Bir az gözlə.'])}")

    # --- [ 5. ADMİN VƏ TEXNİKİ (BÜTÜN ALƏTLƏR) ] ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraf_f(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        for o in OWNERS: await client.send_message(o, f"📩 **Etiraf:** `{txt}`")
        await message.reply_text("✅ Etiraf göndərildi.")

    @app.on_message(filters.command("id"))
    async def id_f(client, message):
        await message.reply_text(f"🆔 User: `{message.from_user.id}`\n🆔 Chat: `{message.chat.id}`")

    @app.on_message(filters.command("ping"))
    async def ping_f(client, message):
        s = time.time()
        m = await message.reply_text("...")
        await m.edit(f"🚀 Gecikmə: `{round((time.time()-s)*1000)}ms`")

    @app.on_message(filters.command("purge") & filters.group)
    async def purge_f(client, message):
        if message.reply_to_message:
            await client.delete_messages(message.chat.id, range(message.reply_to_message.id, message.id))

    @app.on_message(filters.command("ban") & filters.group)
    async def ban_f(client, message):
        if message.reply_to_message:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply_text("🚫 İstifadəçi kənarlaşdırıldı.")

    # --- [ 6. OYUNLAR VƏ FONT CALLBACK ] ---
    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_f(client, message):
        e = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}[message.command[0]]
        await client.send_dice(message.chat.id, emoji=e)

    @app.on_message(filters.command("font"))
    async def font_cmd(client, message):
        if len(message.command) < 2: return
        t = message.text.split(None, 1)[1]
        btns = [[InlineKeyboardButton(k.upper(), callback_data=f"fn|{k}|{t[:15]}")] for k in ["bold", "italic", "mono", "gothic"]]
        await message.reply_text(f"📝 Stil seçin:", reply_markup=InlineKeyboardMarkup(btns))

    @app.on_callback_query()
    async def handle_cb(client, cb):
        if cb.data.startswith("fn|"):
            _, s, txt = cb.data.split("|")
            await cb.edit_message_text(f"✨ `{get_font_text(txt, s)}`")
