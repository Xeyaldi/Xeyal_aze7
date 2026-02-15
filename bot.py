import os, asyncio, random, psycopg2, requests
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# SAHİBƏ VƏ OWNER ID-LƏRİ
OWNERS = [6241071228, 7592728364, 8024893255] 
SAHIBE_ID = 7592728364 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}
chatbot_status = {}
link_block_status = {}

# ----------------- SİYAHLAR (TAM VERSİYA - TOXUNULMADI) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
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
    cur.execute("CREATE TABLE IF NOT EXISTS qadaga_list (word TEXT PRIMARY KEY)")
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
        [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url=f"tg://user?id={SAHIBE_ID}"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
        [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
    ]
    
    await message.reply_photo(
        photo=SAKIL_LINKI, 
        caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- SAHİBƏ PANELİ ---
@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("⚠️ Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər", show_alert=True)
    
    try:
        await callback_query.message.edit_caption(
            caption=(
                "✨ **sᴀʜɪʙə ÖZƏL PANEL**\n\n"
                "📢 **Broadcast:** `/yonlendir` ilə mesaj atın.\n"
                "🚫 **Qadağa:** `/qadaga [söz]` yazaraq qadağan edin."
            ),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri Qayıt", callback_data="back_home")]])
        )
    except:
        await callback_query.answer("Artıq paneldəsiniz!")

@app.on_callback_query(filters.regex("back_home"))
async def back_home(client, callback_query):
    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url=f"tg://user?id={SAHIBE_ID}"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
        [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
    ]
    await callback_query.message.edit_caption(
        caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- QADAGA SİSTEMİ ---
@app.on_message(filters.command("qadaga"))
async def qadaga_cmd(client, message):
    if message.from_user.id not in OWNERS:
        return await message.reply_text("⚠️ **Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər**")
    
    if len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa qadağan ediləcək sözü yazın.\nNümunə: `/qadaga soyus`")
    
    word = message.text.split(None, 1)[1].lower()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO qadaga_list (word) VALUES (%s) ON CONFLICT DO NOTHING", (word,))
    conn.commit()
    cur.close()
    conn.close()
    await message.reply_text(f"✅ **{word}** sözü qadağan olunanlara əlavə edildi.")

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
    await status_msg.edit(f"✅ Yönləndirmə tamamlandı: {success} yerə göndərildi.")

# --- HELP (YENİLƏNDİ - HƏR ŞEY DAXİL) ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "📚 **BOTUN KOMANDALARI**\n\n"
        "🎮 **ƏYLƏNCƏLİ OYUNLAR:** /basket, /futbol, /dart, /slot, /dice\n\n"
        "🌍 **MƏLUMAT:**\n"
        "• /hava [şəhər] - Hava durumu\n"
        "• /valyuta - Günlük məzənə\n"
        "• /id - ID göstərər\n\n"
        "📢 **TAĞ KOMANDALARI:**\n"
        "• /tag - Brilyant tağ\n"
        "• /utag - Emoji tağ\n"
        "• /flagtag - Bayraq tağ\n"
        "• /tektag - Təkli tağ\n\n"
        "🛑 **DAYANDIRMAQ:** /tagstop\n"
        "💬 **CHATBOT:** /chatbot on/off\n"
        "🛡 **ADMİN:** /purge (mesajları silər), /link on/off"
    )
    await message.reply_text(help_text)

# --- CHATBOT ON/OFF ---
@app.on_message(filters.command("chatbot"))
async def chatbot_toggle(client, message):
    if not await is_admin(client, message): return
    if len(message.command) < 2:
        return await message.reply_text("**İstifadə:** `/chatbot on` və ya `/chatbot off`")
    
    status = message.command[1].lower()
    if status == "on":
        chatbot_status[message.chat.id] = True
        await message.reply_text("**✅ Chatbot aktiv edildi!**")
    elif status == "off":
        chatbot_status[message.chat.id] = False
        await message.reply_text("**❌ Chatbot söndürüldü!**")

# --- TAĞ SİSTEMİ ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]))
async def tag_handler(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("**❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!**")
    if not await is_admin(client, message):
        return
    
    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0]
    await message.reply_text(f"**✅ {cmd} başladı!**")
    
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

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await is_admin(client, message):
        return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

# --- YENİ VİZYON KOMANDALARI (HAVA, VALYUTA, LİNK) ---
@app.on_message(filters.command("hava"))
async def get_weather_cmd(client, message):
    if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın. Məsələn: /hava Baki")
    city = message.command[1]
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b6907d289e10d714a6e88b30761fae22&units=metric&lang=az").json()
        await message.reply_text(f"🌤 **{city.capitalize()}**\n🌡 Temperatur: {r['main']['temp']}°C\n☁️ Vəziyyət: {r['weather'][0]['description']}")
    except: await message.reply_text("❌ Xəta: Şəhər tapılmadı.")

@app.on_message(filters.command("valyuta"))
async def get_val_cmd(client, message):
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        usd = 1/r['rates']['USD']
        eur = 1/r['rates']['EUR']
        await message.reply_text(f"💰 **Məzənnə:**\n\n🇺🇸 1 USD = {usd:.2f} AZN\n🇪🇺 1 EUR = {eur:.2f} AZN")
    except: await message.reply_text("❌ Məzənnə alınmadı.")

@app.on_message(filters.command("link"))
async def link_toggle(client, message):
    if not await is_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("/link on və ya /link off")
    status = message.command[1].lower()
    link_block_status[message.chat.id] = (status == "on")
    await message.reply_text(f"🛡 Link qoruması **{status}** edildi.")

# --- CHATBOT LOGIC & QADAGA FILTER ---
@app.on_message(filters.text & ~filters.bot, group=1)
async def message_handler(client, message):
    chat_id = message.chat.id
    text = message.text.lower()

    # Link qoruması yoxla
    if ("http" in text or "t.me" in text) and link_block_status.get(chat_id, False):
        if not await is_admin(client, message):
            await message.delete()
            return

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT word FROM qadaga_list")
    qadagalar = [r[0] for r in cur.fetchall()]
    
    for word in qadagalar:
        if word in text:
            if message.from_user.id not in OWNERS:
                await message.delete()
                cur.close()
                conn.close()
                return

    if chatbot_status.get(chat_id, True) and not message.text.startswith('/'):
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
        if random.random() < 0.2:
            cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
            res = cur.fetchone()
            if res: await message.reply_text(f"**{res[0]}**")
        if "bot" in text:
            await message.reply_text(f"**{random.choice(CB_SOZLER)}**")
            
    conn.commit()
    cur.close()
    conn.close()

# --- OYUNLAR VƏ ID ---
@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice", "id", "stiker", "mute", "purge"]))
async def misc_group_cmds(client, message):
    cmd = message.command[0]
    if cmd == "id":
        return await message.reply_text(f"**🆔 Sizin ID:** `{message.from_user.id}`")
    
    if cmd == "purge" and await is_admin(client, message):
        if message.reply_to_message:
            m_ids = range(message.reply_to_message.id, message.id)
            await client.delete_messages(message.chat.id, m_ids)
            return await message.reply_text("🧹 Təmizləndi!")

    if cmd in ["basket", "futbol", "dart", "slot", "dice"]:
        dice_emoji = {"basket":"🏀","futbol":"⚽","dart":"🎯","slot":"🎰","dice":"🎲"}
        return await client.send_dice(message.chat.id, emoji=dice_emoji[cmd])
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("**❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!**")

# --- STARTUP & COMMAND MENU ---
async def main():
    await app.start()
    # Komanda menyusunu qururuq
    await app.set_bot_commands([
        BotCommand("start", "Botu işə sal"),
        BotCommand("help", "Kömək menyusu"),
        BotCommand("tag", "Brilyant tağ"),
        BotCommand("hava", "Hava durumu"),
        BotCommand("valyuta", "Məzənnə"),
        BotCommand("id", "ID-ni öyrən"),
        BotCommand("purge", "Mesajları təmizlə"),
        BotCommand("link", "Link qoruması on/off")
    ])
    print("Bot tam və düzəlişlərlə aktivdir!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())
