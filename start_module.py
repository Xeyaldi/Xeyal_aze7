import os, asyncio, random, psycopg2, requests, urllib.parse, time
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait

# --- MODULLARI QOŞMAQ ---
try:
    from plugins import init_plugins
except ImportError:
    init_plugins = None

# --- AYARLAR (HEÇ NƏ SİLİNMƏDİ) ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SESSION_STRING = os.getenv("SESSION") 

OWNERS = [6241071228, 7592728364, 8024893255] 
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

tag_process = {}

# --- BOTLARIN QURULMASI ---
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

# --- SƏNİN START MESAJIN (Hec nə silinmədi) ---
def init_start_internal(app):
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        buttons = [
            [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
            [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
        ]
        await message.reply_photo(
            photo=SAKIL_LINKI, 
            caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    @app.on_callback_query(filters.regex("back_home"))
    async def back_home(client, callback_query):
        buttons = [
            [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
            [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
        ]
        await callback_query.message.edit_caption(
            caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# --- AVTOMATİK SKAN FUNKSİYASI ---
@app.on_message(filters.new_chat_members)
async def auto_join_and_scan(client, message):
    for member in message.new_chat_members:
        if member.is_self:
            try:
                invite_link = await client.export_chat_invite_link(message.chat.id)
                await user_app.join_chat(invite_link)
                conn = get_db_connection(); cur = conn.cursor()
                async for msg in user_app.get_chat_history(message.chat.id, limit=5000):
                    if msg.from_user and not msg.from_user.is_bot:
                        cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (message.chat.id, msg.from_user.id))
                conn.commit(); cur.close(); conn.close()
            except: pass

# --- İŞƏ SALMA ---
async def start_bot():
    await app.start()
    if SESSION_STRING:
        try: await user_app.start()
        except: print("Asistant qoşulmadı.")
    
    await app.set_bot_commands([
        BotCommand("start", "Botu başladın"),
        BotCommand("topsiralama", "Top 20 aktivlik"),
        BotCommand("tag", "Tağ et")
    ])
    
    init_start_internal(app) # Sənin start mesajını işə salır
    if init_plugins: init_plugins(app, get_db_connection)
    
    print("🚀 Sistem hazır! Start mesajı və Asistant aktivdir.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
