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

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
SESSION_STRING = os.getenv("SESSION") 

OWNERS = [6241071228, 7592728364, 8024893255] 

# --- DATABASE BAĞLANTISI ---
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# Database-də cədvəlin olub-olmadığını yoxlayan funksiya
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_messages (
            chat_id BIGINT,
            user_id BIGINT,
            msg_count INTEGER DEFAULT 0,
            PRIMARY KEY (chat_id, user_id)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# --- BOTLARIN QURULMASI ---
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

async def is_admin(client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in OWNERS: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

# --- KEÇMİŞİ SKAN EDİB BAZAYA YAZAN FUNKSİYA ---
@app.on_message(filters.command("fullscan") & filters.group)
async def full_scan_history(client, message):
    if not await is_admin(client, message): return
    if not SESSION_STRING:
        return await message.reply_text("❌ `SESSION` tapılmadı.")
    
    chat_id = message.chat.id
    m_status = await message.reply_text("🚀 **Asistant keçmişi skan edir və bazaya yazır...**")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    count = 0
    try:
        async with user_app:
            async for msg in user_app.get_chat_history(chat_id):
                if msg.from_user and not msg.from_user.is_bot:
                    u_id = msg.from_user.id
                    # Bazada məlumatı yeniləyirik (yoxdursa yaradır, varsa üstünə gəlir)
                    cur.execute("""
                        INSERT INTO user_messages (chat_id, user_id, msg_count)
                        VALUES (%s, %s, 1)
                        ON CONFLICT (chat_id, user_id)
                        DO UPDATE SET msg_count = user_messages.msg_count + 1
                    """, (chat_id, u_id))
                    
                    count += 1
                    if count % 500 == 0:
                        conn.commit() # Hər 500 mesajdan bir yaddaşa verir
                        await m_status.edit(f"🔍 Analiz davam edir...\n✅ Bazaya yazıldı: `{count}` mesaj")
        
        conn.commit()
        await m_status.edit(f"✅ **Skan tamamlandı!**\nCəmi `{count}` mesaj bazada yadda saxlanıldı. Artıq deploy etsəniz də silinməyəcək.")
    except Exception as e:
        await m_status.edit(f"❌ Xəta: `{e}`")
    finally:
        cur.close()
        conn.close()

# --- TOP 13 SIRALAMASI (BAZADAN ÇƏKİR) ---
@app.on_message(filters.command("top13") & filters.group)
async def top_13(client, message):
    chat_id = message.chat.id
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT user_id, msg_count FROM user_messages 
        WHERE chat_id = %s 
        ORDER BY msg_count DESC LIMIT 13
    """, (chat_id,))
    
    rows = cur.fetchall()
    if not rows:
        return await message.reply_text("📊 Hələ ki heç bir məlumat yoxdur.")
    
    text = "🏆 **QRUPUN TOP 13-LÜYÜ**\n\n"
    for i, row in enumerate(rows, 1):
        try:
            user = await client.get_users(row[0])
            name = user.first_name
        except:
            name = f"İstifadəçi {row[0]}"
        text += f"{i}. {name} — `{row[1]}` mesaj\n"
    
    await message.reply_text(text)
    cur.close()
    conn.close()

# (Qalan tağ və digər funksiyalar olduğu kimi qalır...)
