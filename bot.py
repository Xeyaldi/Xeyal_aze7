import os, asyncio, random, psycopg2, requests, urllib.parse, time, wikipedia
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SESSION_STRING = os.getenv("SESSION") 

OWNERS = [6241071228, 7592728364, 8024893255] 
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

wikipedia.set_lang("az")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (chat_id BIGINT, user_id BIGINT, msg_count INTEGER DEFAULT 0, PRIMARY KEY (chat_id, user_id));
            CREATE TABLE IF NOT EXISTS user_karma (chat_id BIGINT, user_id BIGINT, karma_count INTEGER DEFAULT 0, PRIMARY KEY (chat_id, user_id))
        """)
        conn.commit(); cur.close(); conn.close()
    except Exception as e: print(f"DB Error: {e}")

tag_process = {}

BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇦","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇰","🇸🇮","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇴","🇹🇷","🇹🇲","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇦","🇻🇪","🇻🇳","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]

async def check_admin(client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in OWNERS: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- START VƏ PANEL ---
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    buttons = [[InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
               [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)]]
    await message.reply_photo(photo=SAKIL_LINKI, caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**", reply_markup=InlineKeyboardMarkup(buttons))

# --- TAĞ SİSTEMİ ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag", "atag"]) & filters.group)
async def tag_handler(client, message):
    if not await check_admin(client, message): return
    tag_process[message.chat.id] = True
    cmd = message.command[0]
    await message.reply_text(f"**✅ {cmd} başladı!**")
    async for m in client.get_chat_members(message.chat.id):
        if not tag_process.get(message.chat.id, False): break
        if m.user and not m.user.is_bot:
            try:
                if cmd == "tag": txt = f"💎 [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "utag": txt = f"{random.choice(EMOJILER)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "flagtag": txt = f"{random.choice(BAYRAQLAR)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "tektag": txt = f"👤 [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "atag": txt = f"✨ @{m.user.username}" if m.user.username else f"👤 [{m.user.first_name}](tg://user?id={m.user.id})"
                await client.send_message(message.chat.id, txt); await asyncio.sleep(2.5)
            except FloodWait as e: await asyncio.sleep(e.value)
            except: pass

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await check_admin(client, message): return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

# --- MESAJ SAYĞACI ---
@app.on_message(filters.group & ~filters.bot, group=-1)
async def global_handler(client, message):
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (message.chat.id, message.from_user.id))
        conn.commit(); cur.close(); conn.close()
    except: pass

# --- OYUNLAR ---
@app.on_message(filters.command(["dice", "slot", "futbol", "basket", "dart"]))
async def games(client, message):
    em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀", "dart":"🎯"}
    await client.send_dice(message.chat.id, emoji=em[message.command[0]])

@app.on_message(filters.command("love"))
async def love_cmd(client, message):
    await message.reply_text(f"❤️ {message.from_user.first_name} və {message.reply_to_message.from_user.first_name} arasında uyğunluq: {random.randint(0, 100)}%")

# --- DİGƏR ---
@app.on_message(filters.command("wiki"))
async def wiki_search(client, message):
    if len(message.command) < 2: return
    query = " ".join(message.command[1:])
    try:
        res = wikipedia.summary(query, sentences=3)
        await message.reply_text(f"📖 **Wiki:** {query}\n\n{res}")
    except: pass

@app.on_message(filters.command("pdf"))
async def pdf_cmd(client, message):
    if not message.reply_to_message: return
    pdf_name = f"doc_{message.from_user.id}.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    if message.reply_to_message.photo:
        p = await message.reply_to_message.download(); c.drawImage(p, 50, 400, 500, 400); os.remove(p)
    elif message.reply_to_message.text:
        c.drawString(100, 750, message.reply_to_message.text[:500])
    c.showPage(); c.save()
    await message.reply_document(pdf_name); os.remove(pdf_name)

# --- HELP (KOMANDALARIN YUXARIDA ÇIXMASI ÜÇÜN) ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    # Bu mesaj boşaldılsa da, slash (/) menusuna bütün komandalar əlavə edilib.
    await message.reply_text("💠 **Komandaları görmək üçün mesaj yerinə / yazıb gözləyin.**")

async def start_bot():
    init_db(); await app.start()
    # Slash (/) menusuna owner olmayan əmrləri əlavə edirik
    await app.set_bot_commands([
        BotCommand("start", "Botu başladın"),
        BotCommand("help", "Kömək menyusu"),
        BotCommand("tag", "Hər kəsi tağ edər"),
        BotCommand("atag", "Username ilə tağ"),
        BotCommand("utag", "Emoji ilə tağ"),
        BotCommand("flagtag", "Bayraq ilə tağ"),
        BotCommand("tagstop", "Tağı dayandırar"),
        BotCommand("wiki", "Wikipedia axtarışı"),
        BotCommand("pdf", "PDF fayl yaradın"),
        BotCommand("dice", "Zər atın"),
        BotCommand("slot", "Slot oyunu"),
        BotCommand("love", "Sevgi testi")
    ])
    if SESSION_STRING:
        try: await user_app.start()
        except: pass
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(start_bot())
