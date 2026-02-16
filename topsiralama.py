import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Bağlantısı - Materialların silinməməsi üçün vacibdir
MONGO_URL = os.environ.get("MONGO_DB_URI")
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db["PersistentStats"]
stats_col = db["group_stats"]

# 📊 MESAJLARI İZLƏMƏ (Nickname ilə)
@Client.on_message(filters.group & ~filters.bot, group=1)
async def track_messages(_, message):
    user_name = message.from_user.first_name # Nickname istifadə olunur
    await stats_col.update_one(
        {"chat_id": message.chat.id, "user_id": message.from_user.id},
        {
            "$inc": {"daily": 1, "weekly": 1, "monthly": 1, "total": 1},
            "$set": {"name": user_name}
        },
        upsert=True
    )

# 🏆 SIRALAMA MƏTNİNİ HAZIRLAYAN FUNKSİYA
async def get_stats_text(chat_id, period_key, period_title):
    # Tam 13 nəfər, Nickname ilə
    top_users = stats_col.find({"chat_id": chat_id, period_key: {"$gt": 0}}).sort(period_key, -1).limit(13)
    
    # Sənin istədiyin dinamik başlıq
    text = f"<b>👥 Qrupunuzda {period_title} ən çox aktiv olanlar:</b>\n\n"
    text += "<b>Kullanıcı → Mesaj</b>\n"
    
    index = 1
    async for user in top_users:
        marker = "🔹" if index <= 3 else "▫️"
        text += f"{marker} {index}. <b>{user['name']}</b> : <code>{user[period_key]}</code>\n"
        index += 1
    
    return text if index > 1 else "<i>Hələ ki, məlumat yoxdur...</i>"

# ⌨️ BUTONLAR (Şəkildəki ardıcıllıqla)
def get_stats_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 Günlük", callback_data="st_daily"),
            InlineKeyboardButton("📊 Həftəlik", callback_data="st_weekly")
        ],
        [
            InlineKeyboardButton("📈 Aylıq", callback_data="st_monthly"),
            InlineKeyboardButton("🌍 Ümumi", callback_data="st_total")
        ],
        [InlineKeyboardButton("📋 Detallı Bilgi", callback_data="st_details")],
        [InlineKeyboardButton("❌ Siyahını Bağla", callback_data="close_stats")]
    ])

@Client.on_message(filters.command(["stats", "topsiralama"]) & filters.group)
async def stats_cmd(_, message):
    text = await get_stats_text(message.chat.id, "daily", "BUGÜN")
    await message.reply_text(text, reply_markup=get_stats_keyboard())

# 🔄 BUTONLARA BASANDA BAŞLIĞIN DƏYİŞMƏSİ
@Client.on_callback_query(filters.regex(r"^st_"))
async def callback_handler(client, query):
    data = query.data.split("_")[1]
    
    # Başlıqlar sənin istədiyin kimi tənzimlənir
    titles = {
        "daily": "BUGÜN",
        "weekly": "BU HƏFTƏ",
        "monthly": "BU AY",
        "total": "ÜMUMİ"
    }
    
    if data in titles:
        new_text = await get_stats_text(query.message.chat.id, data, titles[data])
        # Yalnız mətn dəyişir, köhnə mesaj silinmir
        await query.message.edit_text(new_text, reply_markup=get_stats_keyboard())

@Client.on_callback_query(filters.regex("close_stats"))
async def close_callback(_, query):
    await query.message.delete()
