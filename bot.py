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

chat_status = {}
tag_process = {}

# 250+ BAYRAQLAR (TAM SİYAHI)
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

# 200+ EMOJİLƏR (TAM SİYAHI)
FANCY_EMOJIS = [
    "🌈", "🪐", "🎡", "🍭", "💎", "🔮", "⚡", "🔥", "🚀", "🛸", "🎈", "🎨", "🎭", "🎸", "👾", "🧪", "🧿", "🍀", "🍿", "🎁", 
    "🔋", "🧸", "🎉", "✨", "🌟", "🌙", "☀️", "☁️", "🌊", "🌋", "☄️", "🍄", "🌹", "🌸", "🌵", "🌴", "🍁", "🍎", "🍓", "🍍", 
    "🥥", "🍔", "🍕", "🍦", "🍩", "🥤", "🍺", "🚲", "🏎️", "🚁", "⛵", "🛰️", "📱", "💻", "💾", "📸", "🎥", "🏮", "🎬", 
    "🎧", "🎤", "🎹", "🎺", "🎻", "🎲", "🎯", "🎮", "🧩", "🦄", "🦁", "🦊", "🐼", "🐨", "🐯", "🐝", "🦋", "🦜", "🐬", 
    "🐳", "🐾", "🐉", "🎐", "🎌", "🚩", "🏆", "🎖️", "🎫", "💌", "💍", "👓", "🎒", "👒", "👟", "👗", "👑", "💄", "🧤", "🧶", 
    "🧪", "🧬", "🔭", "📡", "💡", "🕯️", "📚", "📕", "📜", "💵", "💸", "💳", "⚖️", "🗝️", "🔓", "🔨", "🛡️", "🏹", "⚔️", "💊", 
    "🩹", "🩸", "🧺", "🧼", "🧽", "🪒", "🚿", "🛁", "🧻", "🧱", "⛓️", "🧨", "🧧", "🎀", "🎊", "🎐", "🎋", "🎎", "🎏", "🧠", "🦷", 
    "🦴", "👀", "👅", "👄", "👂", "👃", "👣", "👁️‍🗨️", "🗨️", "🧣", "🧥", "👒", "👜", "👛", "👗", "👘", "👖", "👕", "👞", "👟"
]

READY_RESPONSES = ["Necəsən?", "Nə edirsən?", "Mən hər şeyi yadda saxlayıram!", "Azərbaycan dilini sevirəm!"]

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# ----------------- START MESAJI (İSTƏDİYİN KİMİ) -----------------
@app.on_message(filters.command("start"))
async def start(client, message):
    text = (
        "sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ. "
        "ᴋᴏᴍᴜᴛʟᴀʀı öʏʀəɴᴍəᴋ üçüɴ /help ʏᴀᴢᴍᴀğıɴıᴢ ᴋɪғᴀʏəᴛᴅɪʀ."
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]
    ])
    await message.reply_text(text, reply_markup=markup)

# ----------------- HELP VƏ OYUNLAR -----------------
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "🎮 Əʏləncəʟɪ ᴏʏᴜɴʟᴀʀ:\n\n"
        "🏀 /basket - Basketbol\n"
        "⚽ /futbol - Futbol\n"
        "🎯 /dart - Dart\n"
        "🎰 /slot - Slot\n"
        "🎲 /dice - Zar\n\n"
        "📢 Tağ komandaları:\n"
        "🔹 /tag - Normal tağ\n"
        "🔹 /utag - Emoji ilə tağ\n"
        "🔹 /flagtag - Bayraqla tağ\n"
        "🔹 /tektag - Tək-tək tağ\n\n"
        "🛑 Dayandırmaq üçün: /stop\n"
        "💬 Chatbot: /chatbot on/off"
    )
    await message.reply_text(help_text)

@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def play_games(client, message):
    emoji_map = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    await client.send_dice(message.chat.id, emoji=emoji_map[message.command[0]])

# ----------------- TAĞ SİSTEMİ (1.5 SANİYƏ) -----------------
@app.on_message(filters.command("stop") & filters.group)
async def stop_tag(client, message):
    tag_process[message.chat.id] = False
    await message.reply_text("🛑 Tağ prosesi dayandırıldı!")

@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def mass_tag(client, message):
    chat_id = message.chat.id
    tag_process[chat_id] = True
    user_msg = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    cmd = message.command[0].lower()
    
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user)

    if not members:
        return await message.reply_text("❌ Üzv tapılmadı!")

    if cmd == "tektag":
        for user in members:
            if not tag_process.get(chat_id, True): break
            await client.send_message(chat_id, f"{user_msg} [{user.first_name}](tg://user?id={user.id})")
            await asyncio.sleep(1.0)
    else:
        for i in range(0, len(members), 5):
            if not tag_process.get(chat_id, True): break
            chunk = members[i:i+5]
            tag_text = f"📢 {user_msg}\n\n"
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
    
    tag_process[chat_id] = False

# ----------------- CHATBOT (DATABASE ÖYRƏNMƏ) -----------------
@app.on_message(filters.group & ~filters.bot)
async def chat_logic(client, message):
    chat_id = message.chat.id
    try:
        conn = get_db_connection(); cur = conn.cursor()
        m_type = 'text' if message.text else 'sticker' if message.sticker else 'voice'
        content = message.text if message.text else None
        file_id = message.sticker.file_id if message.sticker else message.voice.file_id if message.voice else None
        cur.execute("INSERT INTO brain (msg_type, content, file_id, chat_id, user_id, first_name) VALUES (%s,%s,%s,%s,%s,%s)",
                    (m_type, content, file_id, chat_id, message.from_user.id, message.from_user.first_name))
        conn.commit(); cur.close(); conn.close()
    except: pass

    if random.random() < 0.20 and message.text and not message.text.startswith('/'):
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

@app.on_message(filters.command("chatbot"))
async def toggle_chat(client, message):
    if len(message.command) < 2: return
    status = message.command[1].lower()
    chat_status[message.chat.id] = (status == "on")
    await message.reply_text(f"✅ Chatbot {'Aktiv' if chat_status[message.chat.id] else 'Deaktiv'} edildi!")

app.run()
