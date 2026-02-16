import os, asyncio, random, psycopg2, requests, urllib.parse, time
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait, PeerIdInvalid, RPCError

# --- MODULLARI QOŞMAQ ---
try:
    from plugins import init_plugins 
except ImportError:
    init_plugins = None

try:
    from stats import init_stats
except ImportError:
    init_stats = None

try:
    from start_module import init_start
except ImportError:
    init_start = None

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SESSION_STRING = os.getenv("SESSION") 

OWNERS = [6241071228, 7592728364, 8024893255] 
SOHBET_QRUPU = "sohbetqruprc" 

tag_process = {}
chatbot_status = {} # Chatbotun qrupda aktiv olub-olmadığını yoxlayır
link_block_status = {}

# --- SİYAHLAR (TAM VƏ TOXUNULMAZ) ---
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]

# --- KLİENTLƏR ---
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in OWNERS: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- 🤖 CHATBOT MƏNTİQİ (Əlavə etdim ki, silinmiş olmasın) ---
@app.on_message(filters.text & filters.group & ~filters.bot)
async def chatbot_reply(client, message):
    chat_id = message.chat.id
    if chatbot_status.get(chat_id, False): # Əgər chatbot bu qrupda aktivdirsə
        text = message.text.lower()
        conn = get_db_connection()
        cur = conn.cursor()
        # Bazadan uyğun cavabı axtarırıq
        cur.execute("SELECT reply FROM chatbot_responses WHERE trigger_word = %s", (text,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            await message.reply_text(res[0])

@app.on_message(filters.command("chatbot") & filters.group)
async def toggle_chatbot(client, message):
    if not await is_admin(client, message): return
    chat_id = message.chat.id
    chatbot_status[chat_id] = not chatbot_status.get(chat_id, False)
    status = "Aktiv ✅" if chatbot_status[chat_id] else "Deaktiv ❌"
    await message.reply_text(f"🤖 **Chatbot statusu:** {status}")

# --- FULLSCAN ---
@app.on_message(filters.command("fullscan") & filters.group)
async def full_scan_history(client, message):
    if not await is_admin(client, message): return
    if not SESSION_STRING:
        return await message.reply_text("❌ `SESSION` tapılmadı.")
    
    chat_id = message.chat.id
    target = message.chat.username if message.chat.username else chat_id
    m_status = await message.reply_text("🚀 **Keçmiş skan edilir...**")
    
    count = 0
    try:
        if not user_app.is_connected: await user_app.start()
        async for msg in user_app.get_chat_history(target):
            if msg.from_user and not msg.from_user.is_bot:
                count += 1
        await m_status.edit(f"✅ **Skan tamamlandı!**\nCəmi `{count}` mesaj analiz edildi.")
    except Exception as e:
        await m_status.edit(f"❌ Xəta: `{e}`")

# --- TAĞ SİSTEMLƏRİ ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def tag_handler(client, message):
    if not await is_admin(client, message): return
    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0]
    await message.reply_text(f"**✅ {cmd} başladı!**")
    
    async for m in client.get_chat_members(chat_id):
        if not tag_process.get(chat_id, False): break
        if m.user and not m.user.is_bot:
            try:
                if cmd == "tag": tag_text = f"💎 [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "utag": tag_text = f"{random.choice(EMOJILER)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "flagtag": tag_text = f"{random.choice(BAYRAQLAR)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "tektag": tag_text = f"👤 [{m.user.first_name}](tg://user?id={m.user.id})"
                await client.send_message(chat_id, tag_text)
                await asyncio.sleep(2.5)
            except: pass

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await is_admin(client, message): return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

# --- İŞƏ SALMA ---
async def start_bot():
    await app.start()
    if user_app:
        try: await user_app.start()
        except: pass

    await app.set_bot_commands([
        BotCommand("start", "Botu başladın"),
        BotCommand("topsiralama", "🎖️ Aktivlik Reytinqi"),
        BotCommand("chatbot", "Chatbotu aç/bağla"),
        BotCommand("tag", "Tağ et"),
        BotCommand("id", "ID öyrən")
    ])
    
    if init_start: init_start(app)
    if init_plugins: init_plugins(app, get_db_connection)
    if init_stats: init_stats(app, user_app) # MongoDB Stats
        
    print("Sistem tam olaraq aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
