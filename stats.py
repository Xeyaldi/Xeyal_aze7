import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient

# --- MONDODB BAĞLANTISI (Yaddaşın silinməməsi üçün mütləqdir) ---
MONGO_URL = os.environ.get("MONGO_DB_URI")
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db["PersistentStats"]
stats_col = db["group_stats"]

# --- 📥 1. AVTOMATİK İZLƏMƏ (Bot və Asistan üçün) ---
# Heç bir komanda gözləmədən asistant mesajları anlıq bazaya yazır
@Client.on_message(filters.group & ~filters.bot, group=1)
async def auto_track_messages(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name # ID deyil, Nickname görünür
    
    await stats_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$inc": {"daily": 1, "weekly": 1, "monthly": 1, "total": 1},
            "$set": {"name": user_name}
        },
        upsert=True
    )

# --- 🏆 2. SIRALAMA VƏ ŞƏXSI STATİSTİKA (Fərqli Emojilərlə) ---
async def get_stats_display(chat_id, user_id, user_nick, key, title):
    # Tam 13 nəfərlik limit saxlanıldı
    top_13 = stats_col.find({"chat_id": chat_id, key: {"$gt": 0}}).sort(key, -1).limit(13)
    
    # Şəxsi məlumatları çəkirik
    my_data = await stats_col.find_one({"chat_id": chat_id, "user_id": user_id})
    my_count = my_data[key] if my_data else 0
    
    # Sənin istədiyin fərqli dizayn və emojilər
    res_text = f"<b>🚀 {title} Aktivlik Reytinqi (Top 13)</b>\n\n"
    res_text += "<b>İstifadəçi ✨ Mesaj</b>\n"
    res_text += "──────────────────\n"
    
    count = 1
    async for user in top_13:
        # Şəkildəkindən fərqli markerlər (Fərq bilinsin deyə)
        if count == 1:
            marker = "🥇"
        elif count == 2:
            marker = "🥈"
        elif count == 3:
            marker = "🥉"
        else:
            marker = "🎗️"
            
        res_text += f"{marker} {count}. <b>{user['name']}</b> ➜ <code>{user[key]}</code>\n"
        count += 1
    
    # Ən aşağıda şəxsi statistika hissəsi (Heç nə silinməyib)
    res_text += "──────────────────\n"
    res_text += f"👤 <b>Sənin {user_nick} :</b> <code>{my_count}</code> mesaj"
    
    return res_text

# --- ⌨️ 3. BUTONLAR (Fərqli Emojilərlə) ---
def gen_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Günlük", callback_data="p_daily"), 
            InlineKeyboardButton("📈 Həftəlik", callback_data="p_weekly")
        ],
        [
            InlineKeyboardButton("🌟 Aylıq", callback_data="p_monthly"), 
            InlineKeyboardButton("🌍 Ümumi", callback_data="p_total")
        ],
        [InlineKeyboardButton("✖️ Siyahını Bağla", callback_data="close_stats")]
    ])

# --- 🚀 4. ƏSAS KOMANDA (/topsiralama) ---
@Client.on_message(filters.command(["topsiralama", "stats"]) & filters.group)
async def show_stats(client, message):
    text = await get_stats_display(
        message.chat.id, 
        message.from_user.id, 
        message.from_user.first_name, 
        "daily", 
        "Bugün"
    )
    await message.reply_text(text, reply_markup=gen_buttons())

# --- 🔄 5. DİNAMİK KEÇİD (Başlıqların dəyişməsi) ---
@Client.on_callback_query(filters.regex(r"^p_"))
async def handle_stats_buttons(client, query):
    p_type = query.data.split("_")[1]
    titles = {"daily": "Bugün", "weekly": "Bu Həftə", "monthly": "Bu Ay", "total": "Ümumi"}
    
    if p_type in titles:
        updated_text = await get_stats_display(
            query.message.chat.id, 
            query.from_user.id, 
            query.from_user.first_name, 
            p_type, 
            titles[p_type]
        )
        await query.message.edit_text(updated_text, reply_markup=gen_buttons())

# --- 🗑️ 6. BAĞLAMA ---
@Client.on_callback_query(filters.regex("close_stats"))
async def _close(_, query):
    await query.message.delete()
