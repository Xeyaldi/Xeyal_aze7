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

# --- YENİ STATS SİSTEMİNİN İNTEQRASİYASI ---
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
chatbot_status = {}
link_block_status = {}

# --- SİYAHLAR (TOXUNULMADI) ---
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

# --- FULLSCAN (BOT YOX, ASİSTAN İŞLƏYİR) ---
@app.on_message(filters.command("fullscan") & filters.group)
async def full_scan_history(client, message):
    if not await is_admin(client, message): return
    if not SESSION_STRING:
        return await message.reply_text("❌ `SESSION` tapılmadı.")
    
    chat_id = message.chat.id
    target = message.chat.username if message.chat.username else chat_id
    m_status = await message.reply_text("🚀 **Keçmiş skan edilir...**\n(Asistan keçmişi oxuyur)")
    
    count = 0
    try:
        if not user_app.is_connected:
            await user_app.start()
        
        async for msg in user_app.get_chat_history(target):
            if msg.from_user and not msg.from_user.is_bot:
                # Burada yeni stats sisteminin daxili bazasına əlavə etmə funksiyası çağırıla bilər
                count += 1
                if count % 1000 == 0:
                    try: await m_status.edit(f"🔍 Skan: `{count}` mesaj analiz edildi...")
                    except: pass
        
        await m_status.edit(f"✅ **Skan tamamlandı!**\nCəmi `{count}` mesaj analiz edildi.")
    except Exception as e:
        await m_status.edit(f"❌ Xəta baş verdi: `{e}`")

# --- SAHİBƏ PANELİ ---
@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("⚠️ Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər", show_alert=True)
    await callback_query.message.edit_caption(
        caption="✨ **sᴀʜɪʙə ÖZƏL PANEL**\n\n📢 **Broadcast:** `/yonlendir`", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_home")]])
    )

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

# --- BROADCAST & TEXNİKİ KOMANDALAR ---
@app.on_message(filters.command("yonlendir") & filters.user(OWNERS))
async def broadcast_func(client, message):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM broadcast_list")
    chats = cur.fetchall()
    cur.close()
    conn.close()
    for chat in chats:
        try:
            if message.reply_to_message: await message.reply_to_message.copy(chat[0])
            else: await client.send_message(chat[0], message.text.split(None, 1)[1])
            await asyncio.sleep(0.3)
        except: continue

@app.on_message(filters.command(["id", "ping"]))
async def misc_cmds(client, message):
    if message.command[0] == "id": 
        await message.reply_text(f"🆔 ID: `{message.from_user.id}`")
    else:
        s = time.time()
        m = await message.reply_text("⚡")
        await m.edit(f"🚀 `{int((time.time()-s)*1000)}ms`")

# --- İŞƏ SALMA ---
async def start_bot():
    await app.start()
    if user_app:
        try: await user_app.start()
        except: print("UserBot qoşula bilmədi, amma Bot işləyir.")

    # Komandalar menyusu
    await app.set_bot_commands([
        BotCommand("start", "Botu başladın"),
        BotCommand("help", "📚 Kömək menyusu"),
        BotCommand("fullscan", "Keçmişi skan et (UserBot)"),
        BotCommand("tag", "Brilyant tağ"),
        BotCommand("utag", "Emoji tağ"),
        BotCommand("id", "ID öyrən")
    ])
    
    # Modulların işə salınması (Yeni stats sistemi bura inteqrasiya olundu)
    if init_start: init_start(app)
    if init_plugins: init_plugins(app, get_db_connection)
    if init_stats: init_stats(app, user_app) # MongoDB Stats Sistemi
        
    print("Sistem tam olaraq aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
