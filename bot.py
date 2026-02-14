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

tag_process = {}
chat_status = {}

# ----------------- 250+ BAYRAQLAR (TAM SİYAHI - HEÇ NƏ SİLİNMƏDİ) -----------------
FLAGS = [
    "🇦🇿", "🇹🇷", "🇵🇰", "🇺🇿", "🇰🇿", "🇰🇬", "🇹🇲", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦🇴", "🇦🇮", "🇦🇶", "🇦🇬", "🇦🇷", "🇦🇲", "🇦🇼", "🇦🇺", "🇦🇹",
    "🇧🇸", "🇧🇭", "🇧🇩", "🇧🇧", "🇧🇪", "🇧🇿", "🇧🇯", "🇧🇲", "🇧🇹", "🇧🇴", "🇧🇦", "🇧🇼", "🇧🇷", "🇮🇴", "🇻🇬", "🇧🇳", "🇧🇬", "🇧🇫", "🇧🇮", "🇰🇭",
    "🇨🇲", "🇨🇦", "🇮🇨", "🇨🇻", "🇧🇶", "🇰🇾", "🇨🇫", "🇹🇩", "🇨🇱", "🇨🇳", "🇨🇽", "🇨🇨", "🇨🇴", "🇰🇲", "🇨🇬", "🇨🇩", "🇨🇰", "🇨🇷", "🇨🇮", "🇭🇷",
    "🇨🇺", "🇨🇼", "🇨🇾", "🇨🇿", "🇩🇰", "🇩🇯", "🇩🇲", "🇩🇴", "🇪🇨", "🇪🇬", "🇸🇻", "🇬🇶", "🇪🇷", "🇪🇪", "🇪🇹", "🇪🇺", "🇫🇰", "🇫🇴", "🇫🇯", "🇫🇮",
    "🇫🇷", "🇬🇫", "🇵🇫", "🇹🇫", "🇬🇦", "🇬🇲", "🇬🇪", "🇩🇪", "🇬🇭", "🇬🇮", "🇬🇷", "🇬🇱", "🇬🇩", "🇬🇵", "🇬🇺", "🇬🇹", "🇬🇬", "🇬🇳", "🇬🇼", "🇬🇾",
    "🇭🇹", "🇭🇳", "🇭🇰", "🇭🇺", "🇮🇸", "🇮🇳", "🇮🇩", "🇮🇷", "🇮拉克", "🇮🇪", "🇮🇲", "🇮🇱", "🇮🇹", "🇯🇲", "🇯🇵", "🇯🇪", "🇯🇴", "🇰🇪", "🇰🇮", "🇽🇰",
    "🇰🇼", "🇱🇦", "🇱🇻", "🇱🇧", "🇱🇸", "🇱🇷", "🇱🇾", "🇱🇮", "🇱🇹", "🇱🇺", "🇲🇴", "🇲🇰", "🇲🇬", "🇲🇼", "🇲🇾", "🇲🇻", "🇲🇱", "🇲🇹", "🇲🇭", "🇲🇶",
    "🇲🇷", "🇲🇺", "🇾🇹", "🇲🇽", "🇫🇲", "🇲🇩", "🇲🇨", "🇲🇳", "🇲🇪", "🇲🇸", "🇲🇦", "🇲🇿", "🇲🇲", "🇳🇦", "🇳🇷", "🇳🇵", "🇳🇱", "🇳🇨", "🇳🇿", "🇳🇮",
    "🇳🇪", "🇳🇬", "🇳🇺", "🇳🇫", "🇰🇵", "🇲🇵", "🇳🇴", "🇴🇲", "🇵🇦", "🇵🇬", "🇵🇾", "🇵🇪", "🇵🇭", "🇵🇳", "🇵🇱", "🇵🇹", "🇵🇷", "🇶🇦", "🇷🇪", "🇷🇴",
    "🇷🇺", "🇷🇼", "🇼🇸", "🇸🇲", "🇸🇹", "🇸🇦", "🇸🇳", "🇷🇸", "🇸🇨", "🇸🇱", "🇸🇬", "🇸🇽", "🇸🇰", "🇸🇮", "🇬🇸", "🇸🇧", "🇸🇴", "🇿🇦", "🇰🇷", "🇸🇸",
    "🇪🇸", "🇱🇰", "🇧🇱", "🇸🇭", "🇰🇳", "🇱🇨", "🇵🇲", "🇻🇨", "🇸🇩", "🇸🇷", "🇸🇿", "🇸🇪", "🇨🇭", "🇸🇾", "🇹🇼", "🇹🇯", "🇹🇿", "🇹🇭", "🇹🇱", "🇹🇬",
    "🇹🇰", "🇹🇴", "🇹🇹", "🇹🇳", "🇹🇲", "🇹🇨", "🇹🇻", "🇺🇬", "🇺🇦", "🇦🇪", "🇬🇧", "🇺🇸", "🇺🇾", "🇻🇮", "🇻🇺", "🇻🇦", "🇻🇪", "🇻🇳", "🇼🇫", "🇪🇭",
    "🇾🇪", "🇿🇲", "🇿🇼", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "🏴󠁧󠁢󠁷󠁬󠁳󠁿"
]

# ----------------- 200+ EMOJİLƏR (TAM SİYAHI - HEÇ NƏ SİLİNMƏDİ) -----------------
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

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# ----------------- START MESAJI (ŞƏXSİ VƏ QRUPDA QALDI) -----------------
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    me = await client.get_me()
    text = "sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ."
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{me.username}?startgroup=true")],
        [InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]
    ])
    await message.reply_text(text, reply_markup=markup)

# ----------------- TAĞ KOMANDALARI (BİRBAŞA /tag, /utag və s.) -----------------
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def tagging_handler(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Bu komandanı yalnız adminlər istifadə edə bilər!")

    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0].lower()
    user_msg = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]])
    
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user)

    for user in members:
        if not tag_process.get(chat_id, True): break
        
        if cmd == "flagtag":
            tag_text = f"{user_msg} [{random.choice(FLAGS)}](tg://user?id={user.id})"
        elif cmd == "utag":
            tag_text = f"{user_msg} [{random.choice(FANCY_EMOJIS)}](tg://user?id={user.id})"
        elif cmd == "tektag":
            tag_text = f"{user_msg} [{user.first_name}](tg://user?id={user.id})"
        else: # /tag
            tag_text = f"{user_msg} [💎](tg://user?id={user.id})"
        
        try:
            await client.send_message(chat_id, tag_text, reply_markup=markup)
            await asyncio.sleep(2.0)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except: pass
    
    tag_process[chat_id] = False

# ----------------- TAĞI DAYANDIRMAQ (/tagstop) -----------------
@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tagging(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    tag_process[message.chat.id] = False
    await message.reply_text("🛑 Tağ prosesi dayandırıldı!")

# ----------------- CHATBOT VƏ DİGƏR OYUNLAR (TAM) -----------------
@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def play_games(client, message):
    emoji_map = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    await client.send_dice(message.chat.id, emoji=emoji_map[message.command[0]])

@app.on_message(filters.command("chatbot") & filters.group)
async def set_chatbot(client, message):
    if not await is_admin(client, message.chat.id, message.from_user.id): return
    if len(message.command) < 2: return
    status = message.command[1].lower()
    chat_status[message.chat.id] = (status == "on")
    await message.reply_text(f"✅ Chatbot {'aktiv' if status == 'on' else 'deaktiv'} edildi.")

@app.on_message(filters.group & ~filters.bot)
async def chat_handler(client, message):
    chat_id = message.chat.id
    try:
        if message.text or message.sticker or message.voice:
            conn = get_db_connection(); cur = conn.cursor()
            m_type = 'text' if message.text else 'sticker' if message.sticker else 'voice'
            content = message.text if message.text else None
            file_id = message.sticker.file_id if message.sticker else message.voice.file_id if message.voice else None
            cur.execute("INSERT INTO brain (msg_type, content, file_id, chat_id, user_id, first_name) VALUES (%s,%s,%s,%s,%s,%s)",
                        (m_type, content, file_id, chat_id, message.from_user.id, message.from_user.first_name))
            conn.commit(); cur.close(); conn.close()
    except: pass

    if chat_status.get(chat_id, True):
        if random.random() < 0.20 and message.text and not message.text.startswith('/'):
            try:
                conn = get_db_connection(); cur = conn.cursor()
                cur.execute("SELECT msg_type, content, file_id FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
                res = cur.fetchone()
                if res:
                    if res[0]=='text': await message.reply_text(res[1])
                    elif res[0]=='sticker': await client.send_sticker(chat_id, res[2])
                    elif res[0]=='voice': await client.send_voice(chat_id, res[2])
                cur.close(); conn.close()
            except: pass

app.run()
