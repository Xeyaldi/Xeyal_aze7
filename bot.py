import os, asyncio, random, psycopg2, requests, urllib.parse, time
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait

# --- MODULLARI QOŞMAQ ---
try:
    from plugins import init_plugins, user_stats 
except ImportError:
    init_plugins = None
    user_stats = {}

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
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg"

tag_process = {}
chatbot_status = {}
link_block_status = {}

# --- SİYAHLAR (HEÇ NƏ SİLİNMƏDİ) ---
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱開","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]

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

# --- ASİSTANT SKANER (ORİJİNAL) ---
@app.on_message(filters.new_chat_members)
async def auto_join_and_scan(client, message):
    chat_id = message.chat.id
    for member in message.new_chat_members:
        if member.is_self:
            try:
                invite_link = await client.export_chat_invite_link(chat_id)
                if not user_app.is_connected: await user_app.start()
                await user_app.join_chat(invite_link)
                await client.send_message(chat_id, "✅ **Asistant qoşuldu. Limitsiz skan başladı...**")
                conn = get_db_connection(); cur = conn.cursor()
                count = 0
                async for msg in user_app.get_chat_history(chat_id, limit=None):
                    if msg.from_user and not msg.from_user.is_bot:
                        cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (chat_id, msg.from_user.id))
                        count += 1
                        if count % 1000 == 0: conn.commit()
                conn.commit(); cur.close(); conn.close()
                await client.send_message(chat_id, f"📊 **Skan bitdi!** `{count}` mesaj yazıldı.")
            except: pass

@app.on_message(filters.command("fullscan") & filters.group)
async def full_scan_history(client, message):
    if not await is_admin(client, message): return
    m = await message.reply_text("🚀 **Limitsiz skan edilir...**")
    conn = get_db_connection(); cur = conn.cursor()
    count = 0
    try:
        if not user_app.is_connected: await user_app.start()
        async for msg in user_app.get_chat_history(message.chat.id, limit=None):
            if msg.from_user and not msg.from_user.is_bot:
                cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (message.chat.id, msg.from_user.id))
                count += 1
        conn.commit(); await m.edit(f"✅ Skan tamamlandı: `{count}`")
    except Exception as e: await m.edit(f"❌ Xəta: {e}")
    finally: cur.close(); conn.close()

# --- PANEL VƏ BROADCAST ---
@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("⚠️ Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər", show_alert=True)
    await callback_query.message.edit_caption(
        caption="✨ **sᴀʜɪʙə ÖZƏL PANEL**\n\n📢 **Broadcast:** `/yonlendir`", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_home")]])
    )

@app.on_message(filters.command("yonlendir") & filters.user(OWNERS))
async def broadcast_func(client, message):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT chat_id FROM broadcast_list"); chats = cur.fetchall()
    cur.close(); conn.close()
    for chat in chats:
        try:
            if message.reply_to_message: await message.reply_to_message.copy(chat[0])
            else: await client.send_message(chat[0], message.text.split(None, 1)[1])
        except: continue

# --- TAG SİSTEMİ (BOT.PY-da QALDI) ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def tag_handler(client, message):
    if not await is_admin(client, message): return
    tag_process[message.chat.id] = True
    cmd = message.command[0]
    await message.reply_text(f"**✅ {cmd} başladı!**")
    async for m in client.get_chat_members(message.chat.id):
        if not tag_process.get(message.chat.id, False): break
        if m.user and not m.user.is_bot:
            try:
                if cmd == "tag": txt = f"💎 [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "flagtag": txt = f"{random.choice(BAYRAQLAR)} [{m.user.first_name}](tg://user?id={m.user.id})"
                else: txt = f"{random.choice(EMOJILER)} [{m.user.first_name}](tg://user?id={m.user.id})"
                await client.send_message(message.chat.id, txt); await asyncio.sleep(2.5)
            except: pass

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await is_admin(client, message): return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

async def start_bot():
    await app.start()
    if SESSION_STRING and not user_app.is_connected: await user_app.start()
    if init_plugins: init_plugins(app, get_db_connection)
    print("🚀 Bot aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(start_bot())
