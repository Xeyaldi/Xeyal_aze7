import os, asyncio, random, psycopg2
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# YALNIZ TƏK OWNER ID QALDI
OWNERS = [8024893255] 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}
chatbot_status = {}

# ----------------- SİYAHLAR (TOXUNULMADI) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]
CB_SOZLER = ["Salam","Necəsən?","Nə var nə yox?","Hardasan?","Xoş gəldin","Sağ ol","Buyur","Bəli","Xeyr","Əlbəttə","Can","Nolsun?","Gözəl","Bomba kimi","İşdəyəm","Evdəyəm","Yoldayam","Nə edirsən?","Heç nə","Sən nə edirsən?","Məzələnirsən?","Vay vay","Ay can","Oldu"]

# --- DATABASE ---
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS broadcast_list (chat_id BIGINT PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS brain (content TEXT, chat_id BIGINT)")
    conn.commit()
    cur.close()
    conn.close()

init_db()

# --- ADMIN YOXLAMASI ---
async def is_admin(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return True
    if message.from_user and message.from_user.id in OWNERS:
        return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False

# --- START MESAJI ---
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO broadcast_list (chat_id) VALUES (%s) ON CONFLICT DO NOTHING", (message.chat.id,))
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass

    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("🧑‍💻 sᴀʜɪʙ", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")],
        [InlineKeyboardButton("📢 ʙᴏᴛ ᴋᴀɴᴀʟı", url="https://t.me/ht_bots"), InlineKeyboardButton("🆘 ᴋöᴍəᴋ ǫʀᴜᴘᴜ", url="https://t.me/ht_bots_chat")],
        [InlineKeyboardButton("🛠 sᴀʜɪʙ əᴍʀɪ", callback_data="owner_panel")]
    ]
    
    await message.reply_photo(
        photo=SAKIL_LINKI, 
        caption="sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.\nᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- SAHİB PANELİ ---
@app.on_callback_query(filters.regex("owner_panel"))
async def owner_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("❌ Bu bölmə üçün yetkiniz yoxdur!", show_alert=True)
    
    await callback_query.edit_message_caption(
        caption=(
            "✨ **🧑‍💻 sᴀʜɪʙ ÖZƏL PANEL**\n\n"
            "📢 **Yönləndirmə (Broadcast) Qaydası:**\n"
            "Mesajı yazıb /yonlendir yazın. Bot həm qruplara, həm də şəxsi yazanlara göndərəcək.\n\n"
            "**Nümunə:** `/yonlendir Salam!`"
        ),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri Qayıt", callback_data="back_home")]])
    )

@app.on_callback_query(filters.regex("back_home"))
async def back_home(client, callback_query):
    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("🧑‍💻 sᴀʜɪʙ", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")],
        [InlineKeyboardButton("📢 ʙᴏᴛ ᴋᴀɴᴀʟı", url="https://t.me/ht_bots"), InlineKeyboardButton("🆘 ᴋöᴍəᴋ ǫʀᴜᴘᴜ", url="https://t.me/ht_bots_chat")],
        [InlineKeyboardButton("🛠 sᴀʜɪʙ əᴍʀɪ", callback_data="owner_panel")]
    ]
    await callback_query.edit_message_caption(
        caption="sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.\nᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- YÖNLƏNDİRMƏ ---
@app.on_message(filters.command("yonlendir") & filters.user(OWNERS))
async def broadcast_func(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa yönləndiriləcək mesajı yazın!")
    
    status_msg = await message.reply_text("📢 Mesaj hər kəsə yönləndirilir...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM broadcast_list")
    chats = cur.fetchall()
    cur.close()
    conn.close()

    success = 0
    for chat in chats:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(chat[0])
            else:
                await client.send_message(chat[0], message.text.split(None, 1)[1])
            success += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            continue
    await status_msg.edit(f"✅ Yönləndirmə tamamlandı: {success} yerə (Qrup+Şəxsi) göndərildi.")

# --- HELP ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!")
    help_text = (
        "🎮 **ƏYLƏNCƏLİ OYUNLAR:** /basket, /futbol, /dart, /slot, /dice\n\n"
        "📢 **TAĞ KOMANDALARI:**\n"
        "/tag, /utag, /flagtag, /tektag\n\n"
        "🛑 **DAYANDIRMAQ:** /tagstop\n"
        "💬 **CHATBOT:** /chatbot on/off\n"
        "🆔 **ID ÖYRƏNMƏK:** /id"
    )
    await message.reply_text(help_text)

# --- TAĞ SİSTEMİ ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]))
async def tag_handler(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!")
    if not await is_admin(client, message):
        return
    
    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0]
    await message.reply_text(f"✅ {cmd} başladı!")
    
    async for m in client.get_chat_members(chat_id):
        if not tag_process.get(chat_id, False):
            break
        if m.user and not m.user.is_bot:
            try:
                if cmd == "tag":
                    tag_text = f"💎 [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "utag":
                    tag_text = f"{random.choice(EMOJILER)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "flagtag":
                    tag_text = f"{random.choice(BAYRAQLAR)} [{m.user.first_name}](tg://user?id={m.user.id})"
                elif cmd == "tektag":
                    tag_text = f"👤 [{m.user.first_name}](tg://user?id={m.user.id})"
                
                await client.send_message(chat_id, tag_text)
                await asyncio.sleep(2.5)
            except:
                pass

@app.on_message(filters.command("tagstop"))
async def stop_tag(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!")
    if not await is_admin(client, message):
        return
    tag_process[message.chat.id] = False
    await message.reply_text("🛑 Tağ dayandırıldı.")

# --- CHATBOT ---
@app.on_message(filters.command("chatbot"))
async def chatbot_toggle(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!")
    if not await is_admin(client, message): return
    if len(message.command) < 2:
        return await message.reply_text("İstifadə: `/chatbot on` və ya `/chatbot off`")
    
    status = message.command[1].lower()
    if status == "on":
        chatbot_status[message.chat.id] = True
        await message.reply_text("✅ Chatbot aktiv edildi!")
    elif status == "off":
        chatbot_status[message.chat.id] = False
        await message.reply_text("❌ Chatbot söndürüldü!")

@app.on_message(filters.group & ~filters.bot)
async def chatbot_logic(client, message):
    if not chatbot_status.get(message.chat.id, True): return
    if not message.text or message.text.startswith('/'): return
    
    chat_id = message.chat.id
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
        if random.random() < 0.2:
            cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
            res = cur.fetchone()
            if res: await message.reply_text(res[0])
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass
    
    if "bot" in message.text.lower():
        await message.reply_text(random.choice(CB_SOZLER))

# --- OYUNLAR ---
@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!")
    dice_emoji = {"basket":"🏀","futbol":"⚽","dart":"🎯","slot":"🎰","dice":"🎲"}
    await client.send_dice(message.chat.id, emoji=dice_emoji[message.command[0]])

# --- ID SİSTEMİ (TƏKMİLLƏŞDİRİLMİŞ) ---
@app.on_message(filters.command("id"))
async def get_id(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(f"👤 Sizin ID: `{message.from_user.id}`")
    
    id_text = f"🆔 Qrup ID: `{message.chat.id}`\n"
    id_text += f"👤 Sizin ID: `{message.from_user.id}`"
    
    if message.reply_to_message:
        id_text += f"\n👤 Reply ID: `{message.reply_to_message.from_user.id}`"
        
    await message.reply_text(id_text)

app.run()
