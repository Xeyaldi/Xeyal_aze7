import os, asyncio, psycopg2
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- AYARLAR ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SESSION_STRING = os.getenv("SESSION") 

SOHBET_QRUPU = "https://t.me/sohbetqruprc" 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

try:
    from plugins import init_plugins
except ImportError:
    init_plugins = None

# --- ANA MENYU FUNKSİYASI (Təkrarlanmasın deyə bir yerdə yazırıq) ---
async def get_main_menu(client):
    bot_info = await client.get_me()
    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{bot_info.username}?startgroup=true")],
        [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
        [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
    ]
    return InlineKeyboardMarkup(buttons)

# --- START ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    markup = await get_main_menu(client)
    await message.reply_photo(
        photo=SAKIL_LINKI, 
        caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
        reply_markup=markup
    )

# --- GERİ DÜYMƏSİ (BACK_HOME) ---
@app.on_callback_query(filters.regex("back_home"))
async def back_home_callback(client, callback_query):
    markup = await get_main_menu(client)
    try:
        await callback_query.message.edit_caption(
            caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
            reply_markup=markup
        )
    except:
        await callback_query.answer()

# --- İŞƏ SALMA ---
async def start_bot():
    await app.start()
    if SESSION_STRING:
        try: await user_app.start()
        except: pass

    if init_plugins:
        init_plugins(app, get_db_connection, user_app) # Userbotu da pluginlərə göndəririk
    
    print("🚀 Bot aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(start_bot())
