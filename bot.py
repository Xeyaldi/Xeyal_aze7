import os
import asyncio
import random
import psycopg2
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# Tənzimləmələr
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Botun söhbət vəziyyəti
chat_status = {}

# 250+ DÜNYA BAYRAQLARI
FLAGS = [
    "🇦🇿", "🇹🇷", "🇵🇰", "🇺🇿", "🇰🇿", "🇰🇬", "🇹🇲", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦🇴", "🇦🇮", "🇦🇶", "🇦🇬", "🇦🇷", "🇦🇲", "🇦🇼", "🇦🇺", "🇦🇹",
    "🇧🇸", "🇧🇭", "🇧🇩", "🇧🇧", "🇧🇪", "🇧🇿", "🇧🇯", "🇧🇲", "🇧🇹", "🇧🇴", "🇧🇦", "🇧🇼", "🇧🇷", "🇮🇴", "🇻🇬", "🇧🇳", "🇧🇬", "🇧🇫", "🇧🇮", "🇰🇭",
    "🇨🇲", "🇨🇦", "🇮🇨", "🇨🇻", "🇧🇶", "🇰🇾", "🇨🇫", "🇹🇩", "🇨🇱", "🇨🇳", "🇨🇽", "🇨🇨", "🇨🇴", "🇰🇲", "🇨🇬", "🇨🇩", "🇨🇰", "🇨🇷", "🇨🇮", "🇭🇷",
    "🇨🇺", "🇨🇼", "🇨🇾", "🇨🇿", "🇩🇰", "🇩🇯", "🇩🇲", "🇩🇴", "🇪🇨", "🇪🇬", "🇸🇻", "🇬🇶", "🇪🇷", "🇪🇪", "🇪🇹", "🇪🇺", "🇫🇰", "🇫🇴", "🇫🇯", "🇫🇮",
    "🇫🇷", "🇬🇫", "🇵🇫", "🇹🇫", "🇬🇦", "🇬🇲", "🇬🇪", "🇩🇪", "🇬🇭", "🇬🇮", "🇬🇷", "🇬🇱", "🇬🇩", "🇬🇵", "🇬🇺", "🇬🇹", "🇬🇬", "🇬🇳", "🇬🇼", "🇬🇾",
    "🇭🇹", "🇭🇳", "🇭🇰", "🇭🇺", "🇮🇸", "🇮🇳", "🇮🇩", "🇮🇷", "🇮🇶", "🇮🇪", "🇮🇲", "🇮🇱", "🇮🇹", "🇯🇲", "🇯🇵", "🇯🇪", "🇯🇴", "🇰🇪", "🇰🇮", "🇽🇰",
    "🇰🇼", "🇱🇦", "🇱🇻", "🇱🇧", "🇱🇸", "🇱🇷", "🇱🇾", "🇱🇮", "🇱🇹", "🇱🇺", "🇲🇴", "🇲🇰", "🇲🇬", "🇲🇼", "🇲🇾", "🇲🇻", "🇲🇱", "🇲🇹", "🇲🇭", "🇲🇶",
    "🇲🇷", "🇲🇺", "🇾🇹", "🇲🇽", "🇫🇲", "🇲🇩", "🇲🇨", "🇲🇳", "🇲🇪", "🇲🇸", "🇲🇦", "🇲🇿", "🇲🇲", "🇳🇦", "🇳🇷", "🇳🇵", "🇳🇱", "🇳🇨", "🇳🇿", "🇳🇮",
    "🇳🇪", "🇳🇬", "🇳🇺", "🇳🇫", "🇰🇵", "🇲🇵", "🇳🇴", "🇴🇲", "🇵🇦", "🇵🇬", "🇵🇾", "🇵🇪", "🇵🇭", "🇵🇳", "🇵🇱", "🇵🇹", "🇵🇷", "🇶🇦", "🇷🇪", "🇷🇴",
    "🇷🇺", "🇷🇼", "🇼🇸", "🇸🇲", "🇸🇹", "🇸🇦", "🇸🇳", "🇷🇸", "🇸🇨", "🇸🇱", "🇸🇬", "🇸🇽", "🇸🇰", "🇸🇮", "🇬🇸", "🇸🇧", "🇸🇴", "🇿🇦", "🇰🇷", "🇸🇸",
    "🇪🇸", "🇱🇰", "🇧🇱", "🇸🇭", "🇰🇳", "🇱🇨", "🇵🇲", "🇻🇨", "🇸🇩", "🇸🇷", "🇸🇿", "🇸🇪", "🇨🇭", "🇸🇾", "🇹🇼", "🇹🇯", "🇹🇿", "🇹🇭", "🇹🇱", "🇹🇬",
    "🇹🇰", "🇹🇴", "🇹🇹", "🇹🇳", "🇹🇲", "🇹🇨", "🇹🇻", "🇺🇬", "🇺🇦", "🇦🇪", "🇬🇧", "🇺🇸", "🇺🇾", "🇻🇮", "🇻🇺", "🇻🇦", "🇻🇪", "🇻🇳", "🇼🇫", "🇪🇭",
    "🇾🇪", "🇿🇲", "🇿🇼", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "🏴󠁧󠁢󠁷󠁬󠁳󠁿"
]

# 200+ RƏNGARƏNG EMOJİ
FANCY_EMOJIS = [
    "🌈", "🪐", "🎡", "🍭", "💎", "🔮", "⚡", "🔥", "🚀", "🛸", "🎈", "🎨", "🎭", "🎸", "👾", "🧪", "🧿", "🍀", "🍿", "🎁", 
    "🔋", "🧸", "🎉", "✨", "🌟", "🌙", "☀️", "☁️", "🌊", "🌋", "☄️", "🍄", "🌹", "🌸", "🌵", "🌴", "🍁", "🍎", "🍓", "🍍", 
    "🥥", "🍔", "🍕", "🍦", "🍩", "🥤", "🍺", "🚲", "🏎️", "🚁", "⛵", "🛰️", "📱", "💻", "💾", "📸", "🎥", "🏮", "🎬", 
    "🎧", "🎤", "🎹", "🎺", "🎻", "🎲", "🎯", "🎮", "🧩", "🦄", "🦁", "🦊", "🐼", "🐨", "🐯", "🐝", "🦋", "🦜", "🐬", 
    "🐳", "🐾", "🐉", "🎐", "🎌", "🚩", "🏆", "🎖️", "🎫", "💌", "💍", "👓", "🎒", "👒", "👟", "👗", "👑", "💄", "🧤", "💍", 
    "🧶", "🧪", "🧬", "🔭", "📡", "💡", "🕯️", "📚", "📕", "📜", "💵", "💸", "💳", "💎", "⚖️", "🗝️", "🔓", "🔨", "🛡️", "🏹", 
    "⚔️", "💊", "🩹", "🩸", "🧺", "🧼", "🧽", "🪒", "🚿", "🛁", "🧸", "🪞", "🧹", "🧺", "🧻", "🏮", "🧱", "⛓️", "🔭", "🩹", 
    "🧨", "🎈", "🧧", "🎀", "🎊", "🎐", "🎋", "🎎", "🎏", "🧠", "🦷", "🦴", "👀", "👅", "👄", "👂", "👃", "👣", "👁️‍🗨️", "🗨️", 
    "🧤", "🧣", "🧥", "👒", "👜", "👛", "👗", "👘", "👖", "👕", "👞", "👟", "👢", "👠", "👡", "🧤", "🧣", "🧶", "🧵", "🌑", "🌒", 
    "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "🌡️", "🌤️", "🌥️", "🌦️", "🌧️", "🌨️", "🌩️", "🌪️", "🌫️", "🌬️"
]

# 200+ HAZIR SÖHBƏT CAVABLARI
READY_RESPONSES = [
    "Necəsən?", "Nə edirsən?", "Səninlə söhbət etmək maraqlıdır.", "Mən hər şeyi yadda saxlayıram!", 
    "Sən çox ağıllısan.", "Buna inanmıram!", "Doğurdan?", "Bəli, tamamilə razıyam.", "Xeyr, mən belə düşünmürəm.",
    "Gəl başqa mövzudan danışaq.", "Mən bir süni intellektəm!", "Azərbaycan dilini çox sevirəm!", 
    "Qrupda maraqlı söhbətlər gedir.", "Dost olaq?", "Sənin adın çox qəşəngdir.", "Mən həmişə buradayam.",
    "Mənə bir sirr de.", "Səni izləyirəm 👀", "Gülməli bir şey de.", "Həyat maraqlıdır!", "Nə xəbər var?",
    "Bu gün çox yaraşıqlısan (və ya gözəlsən)!", "Məni kim yaradıb?", "Özünə yaxşı bax.", "Hər şey qaydasındadır?"
]

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# ----------------- START & HELP -----------------
@app.on_message(filters.command("start"))
async def start(client, message):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]
    ])
    await message.reply_text("sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ. ᴋᴏᴍᴜᴛʟᴀʀı öʏʀəɴᴍəᴋ üçüɴ  /help ʏᴀᴢᴍᴀğıɴıᴢ ᴋɪғᴀʏəᴛᴅɪʀ.", reply_markup=markup)

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = """
✨ **ʙᴏᴛᴜɴ ᴋᴏᴍᴜᴛʟᴀʀɪ:**
🔸 `/tektag` - Hər kəsi tək-tək tağ edər.
🔸 `/utag` - Emoji ilə tağ.
🔸 `/flagtag` - Bayraqlarla tağ.
🔸 `/tag` - 5-5 tağ.
🔸 `/chatbot on/off` - Söhbəti aktiv/deaktiv et.
    """
    await message.reply_text(help_text)

# ----------------- CHATBOT ON/OFF -----------------
@app.on_message(filters.command("chatbot"))
async def toggle_chat(client, message):
    if len(message.command) < 2: return
    status = message.command[1].lower()
    chat_status[message.chat.id] = (status == "on")
    await message.reply_text(f"✅ Chatbot {'Aktiv' if chat_status[message.chat.id] else 'Deaktiv'} edildi!")

# ----------------- MASS TAG (PROFESSIONAL SİSTEM) -----------------
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def mass_tag(client, message):
    chat_id = message.chat.id
    user_msg = " ".join(message.command[1:]) if len(message.command) > 1 else "Diqqət!"
    cmd = message.command[0].lower()
    
    # Bütün üzvləri dərhal Telegram-dan çəkir (Pyrogram-ın üstünlüyü)
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user)

    if not members:
        await message.reply_text("❌ Heç bir üzv tapılmadı. Məni Admin edin!")
        return

    if cmd == "tektag":
        for user in members:
            await client.send_message(chat_id, f"{user_msg} [{user.first_name}](tg://user?id={user.id})")
            await asyncio.sleep(0.8)
    else:
        for i in range(0, len(members), 5):
            chunk = members[i:i+5]
            tag_text = f"📢 **{user_msg}**\n\n"
            for user in chunk:
                if cmd == "flagtag": icon = random.choice(FLAGS)
                elif cmd == "utag": icon = random.choice(FANCY_EMOJIS)
                else: icon = "💎"
                tag_text += f"{icon} [{user.first_name}](tg://user?id={user.id}) "
            
            try:
                await client.send_message(chat_id, tag_text)
                await asyncio.sleep(1.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)

# ----------------- CHATBOT & ÖYRƏNMƏ -----------------
@app.on_message(filters.group & ~filters.bot)
async def chat_logic(client, message):
    chat_id = message.chat.id
    
    # Mesajı bazaya yadda saxla (Öyrənmə hissəsi)
    try:
        conn = get_db_connection(); cur = conn.cursor()
        m_type = 'text' if message.text else 'sticker' if message.sticker else 'voice'
        content = message.text if message.text else None
        file_id = message.sticker.file_id if message.sticker else message.voice.file_id if message.voice else None
        
        cur.execute("INSERT INTO brain (msg_type, content, file_id, chat_id, user_id, first_name) VALUES (%s,%s,%s,%s,%s,%s)",
                    (m_type, content, file_id, chat_id, message.from_user.id, message.from_user.first_name))
        conn.commit(); cur.close(); conn.close()
    except: pass

    # Cavab vermə ehtimalı (20%)
    if chat_status.get(chat_id, True) and random.random() < 0.20:
        if random.choice(["ready", "learned"]) == "ready":
            await message.reply_text(random.choice(READY_RESPONSES))
        else:
            try:
                conn = get_db_connection(); cur = conn.cursor()
                cur.execute("SELECT msg_type, content, file_id FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
                res = cur.fetchone()
                if res:
                    if res[0]=='text' and res[1]: await message.reply_text(res[1])
                    elif res[0]=='sticker': await client.send_sticker(chat_id, res[2])
                    elif res[0]=='voice': await client.send_voice(chat_id, res[2])
                cur.close(); conn.close()
            except: pass

app.run()
