import os, asyncio, random, psycopg2, requests, urllib.parse, time, importlib
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait

# --- PLUGİNS FAYLINI TANIMAQ ÜÇÜN KÖRPÜ (YENİ) ---
def load_plugins(client):
    # plugin.py faylı varsa onu yükləyir
    if os.path.exists("plugin.py"):
        try:
            importlib.import_module("plugin")
            print("✅ plugin.py tanındı!")
        except Exception as e:
            print(f"❌ plugin.py xətası: {e}")
    
    # plugins qovluğu varsa içindəki hər şeyi yükləyir
    if os.path.exists("plugins"):
        for file in os.listdir("plugins"):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = f"plugins.{file[:-3]}"
                try:
                    importlib.import_module(module_name)
                except:
                    pass

# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

OWNERS = [6241071228, 7592728364, 8024893255] 
SAHIBE_ID = 7592728364 
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}
chatbot_status = {}
link_block_status = {}

# ----------------- SİYAHLAR (HEÇ NƏ SİLİNMƏYİB) -----------------
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
    cur.execute("CREATE TABLE IF NOT EXISTS user_history (user_id BIGINT, old_name TEXT, old_username TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS user_stats (user_id BIGINT PRIMARY KEY, msg_count INT DEFAULT 0)")
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
        [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
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
        [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
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
        return await message.reply_text("Zəhmət olmasa qadağan ediləcək sözü yazın.")
    
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

# --- HELP ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "📚 **BOTUN KOMANDALARI**\n\n"
        "🎮 **ƏYLƏNCƏLİ OYUNLAR:** /basket, /futbol, /dart, /slot, /dice\n\n"
        "🌍 **MƏLUMAT:**\n"
        "• /hava [şəhər] - Hava durumu\n"
        "• /valyuta - Günlük məzənə\n"
        "• /id - ID göstərər\n"
        "• /info - İstifadəçi məlumatı\n"
        "• /tercume [dil] - (Reply) Tərcümə edər\n"
        "• /wiki [mövzu] - Vikipediya axtarışı\n"
        "• /namaz [şəhər] - Namaz vaxtları\n\n"
        "📢 **TAĞ KOMANDALARI:**\n"
        "• /tag - Brilyant tağ\n"
        "• /utag - Emoji tağ\n"
        "• /flagtag - Bayraq tağ\n"
        "• /tektag - Təkli tağ\n\n"
        "🤫 **ETİRAFLAR:**\n"
        "• /etiraf [mesaj] - Anonim etiraf\n"
        "• /acetiraf [mesaj] - Açıq etiraf\n\n"
        "🛑 **DAYANDIRMAQ:** /tagstop\n"
        "💬 **CHATBOT:** /chatbot on/off\n"
        "🛡 **ADMİN:** /purge, /link on/off, /ping"
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

# --- HAVA, VALYUTA, LİNK ---
@app.on_message(filters.command("hava"))
async def get_weather_cmd(client, message):
    if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın.")
    city = message.command[1]
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid=b6907d289e10d714a6e88b30761fae22&units=metric&lang=az").json()
        await message.reply_text(f"🌤 **{city.capitalize()}**\n🌡 Temperatur: {r['main']['temp']}°C\n☁️ Vəziyyət: {r['weather'][0]['description']}")
    except: await message.reply_text("❌ Şəhər tapılmadı.")

@app.on_message(filters.command("valyuta"))
async def get_val_cmd(client, message):
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 **Məzənnə:**\n\n🇺🇸 1 USD = {1/r['rates']['USD']:.2f} AZN\n🇪🇺 1 EUR = {1/r['rates']['EUR']:.2f} AZN")
    except: await message.reply_text("❌ Məzənnə alınmadı.")

@app.on_message(filters.command("link"))
async def link_toggle(client, message):
    if not await is_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("/link on/off")
    status = message.command[1].lower()
    link_block_status[message.chat.id] = (status == "on")
    await message.reply_text(f"🛡 Link qoruması **{status}** edildi.")

# --- CHATBOT LOGIC ---
@app.on_message(filters.text & ~filters.bot, group=1)
async def message_handler(client, message):
    chat_id = message.chat.id
    text = message.text.lower()
    uid = message.from_user.id
    fname = message.from_user.first_name
    uname = message.from_user.username or "Yoxdur"

    if ("http" in text or "t.me" in text) and link_block_status.get(chat_id, False):
        if not await is_admin(client, message):
            await message.delete()
            return

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT old_name FROM user_history WHERE user_id = %s ORDER BY date DESC LIMIT 1", (uid,))
    last = cur.fetchone()
    if not last or last[0] != fname:
        cur.execute("INSERT INTO user_history (user_id, old_name, old_username) VALUES (%s, %s, %s)", (uid, fname, uname))
    
    cur.execute("INSERT INTO user_stats (user_id, msg_count) VALUES (%s, 1) ON CONFLICT (user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (uid,))

    cur.execute("SELECT word FROM qadaga_list")
    qadagalar = [r[0] for r in cur.fetchall()]
    for word in qadagalar:
        if word in text:
            if message.from_user.id not in OWNERS:
                await message.delete()
                cur.close(); conn.close()
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
    cur.close(); conn.close()

# --- TƏRCÜMƏ ---
@app.on_message(filters.command("tercume") & filters.reply)
async def translate_msg(client, message):
    text = message.reply_to_message.text
    if not text: return
    
    if len(message.command) > 1:
        target_lang = message.command[1].lower()
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
            r = requests.get(url).json()
            await message.reply_text(f"🌐 **{target_lang.upper()}:**\n`{r[0][0][0]}`")
        except: await message.reply_text("❌ Xəta.")
    else:
        langs = {"en": "🇬🇧 EN", "tr": "🇹🇷 TR", "ru": "🇷🇺 RU", "de": "🇩🇪 DE", "fr": "🇫🇷 FR"}
        res = "🌐 **5 Dilə Tərcümə:**\n\n"
        for code, name in langs.items():
            try:
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={code}&dt=t&q={urllib.parse.quote(text)}"
                r = requests.get(url).json()
                res += f"🔹 {name}: `{r[0][0][0]}`\n"
            except: continue
        await message.reply_text(res)

# --- VİKİPEDİYA (DAHADA TƏKMİLLƏŞMİŞ VƏ LİNKSİZ) ---
@app.on_message(filters.command("wiki"))
async def wiki_search(client, message):
    if len(message.command) < 2:
        return await message.reply_text("🔍 Mövzunu yazın.")

    query = message.text.split(None, 1)[1]

    try:
        # 1️⃣ AXTARIŞ (AZ Wikipedia)
        url = "https://az.wikipedia.org/w/api.php"
        headers = {"User-Agent": "Mozilla/5.0"}

        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        search_r = requests.get(
            url,
            params=search_params,
            headers=headers,
            timeout=10
        ).json()

        results = search_r.get("query", {}).get("search", [])
        if not results:
            return await message.reply_text("❌ Məlumat tapılmadı.")

        title_found = results[0]["title"]

        # 2️⃣ XÜLASƏ + ŞƏKİL
        extract_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|pageimages",
            "exintro": True,
            "explaintext": True,
            "titles": title_found,
            "redirects": 1,
            "pithumbsize": 500
        }

        r = requests.get(
            url,
            params=extract_params,
            headers=headers,
            timeout=10
        ).json()

        page = list(r["query"]["pages"].values())[0]

        title = page.get("title", "")
        extract = page.get("extract", "")
        image = page.get("thumbnail", {}).get("source")

        if not extract:
            return await message.reply_text("❌ Xülasə yoxdur.")

        # 3️⃣ AÇIQLAYICI CAVAB (UZUN)
        msg = f"📖 **{title}**\n\n{extract[:2000]}"

        if image:
            await message.reply_photo(photo=image, caption=msg)
        else:
            await message.reply_text(msg)

    except:
        await message.reply_text("⚠️ Wikipedia-dan cavab alınmadı.")

# --- NAMAZ VAXTLARI (SƏNİN İMPORTLARINLA) ---
@app.on_message(filters.command("namaz"))
async def namaz_vaxtlari(client, message):
    # Əgər şəhər yazılmayıbsa Bakı götürür
    city = message.command[1] if len(message.command) > 1 else "Baku"
    
    try:
        # Namaz vaxtları API
        url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        r = requests.get(url, headers=headers, timeout=10).json()
        
        if 'data' not in r:
            return await message.reply_text("❌ Şəhər tapılmadı (İngiliscə yazın. Məs: /namaz Ganja)")
            
        t = r['data']['timings']
        
        # Səliqəli format
        res = (
            f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n"
            f"🌅 Sübh: `{t['Fajr']}`\n"
            f"☀️ Günəş: `{t['Sunrise']}`\n"
            f"🕛 Zöhr: `{t['Dhuhr']}`\n"
            f"🕒 Əsr: `{t['Asr']}`\n"
            f"🌇 Axşam: `{t['Maghrib']}`\n"
            f"🌃 İşа: `{t['Isha']}`"
        )
        await message.reply_text(res)
        
    except Exception:
        await message.reply_text("⚠️ Namaz vaxtlarını gətirmək mümkün olmadı.")                        
# --- ETİRAF TƏSDİQ SİSTEMİ (YENİ) ---
@app.on_message(filters.command(["etiraf", "acetiraf"]))
async def etiraf_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa etirafınızı yazın.")
    
    is_anon = "Anonim" if message.command[0] == "etiraf" else f"Açıq ({message.from_user.mention})"
    etiraf_text = message.text.split(None, 1)[1]
    
    # Sahibəyə düymələr göndərilir
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"approve_etiraf|{message.chat.id}"),
            InlineKeyboardButton("❌ Rədd et", callback_data="decline_etiraf")
        ]
    ])
    
    await client.send_message(
        SAHIBE_ID, 
        f"🔔 **Yeni Etiraf Gəldi!**\n\n**Növ:** {is_anon}\n**Etiraf:**\n`{etiraf_text}`",
        reply_markup=keyboard
    )
    await message.reply_text("✅ Etirafınız sahibəyə göndərildi. Təsdiq edildikdən sonra paylaşılacaq.")

@app.on_callback_query(filters.regex(r"^(approve_etiraf|decline_etiraf)"))
async def process_etiraf_callback(client, callback_query):
    if callback_query.from_user.id != SAHIBE_ID:
        return await callback_query.answer("Sən sahibə deyilsən!", show_alert=True)
    
    action = callback_query.data.split("|")[0]
@app.on_callback_query(filters.regex(r"^(approve_etiraf|decline_etiraf)"))
async def process_etiraf_callback(client, callback_query):
    if callback_query.from_user.id != SAHIBE_ID:
        return await callback_query.answer("Sən sahibə deyilsən!", show_alert=True)

    # 410-cu sətir - İndi funksiyanın daxilindədir
    action = callback_query.data.split("|")[0]

    if action == "approve_etiraf":
        # Etiraf mətnini mesajdan çıxarırıq
        et_msg = callback_query.message.text.split("Etiraf:\n")[1]
        header = "🤫 **Anonim Etiraf**" if "Anonim" in callback_query.message.text else "📢 **Açıq Etiraf**"
        
        # Qrupa göndər
        qrup_user = SOHBET_QRUPU.split('/')[-1]
        await client.send_message(qrup_user, f"{header}:\n\n`{et_msg}`")
        await callback_query.message.edit_text("✅ Etiraf təsdiqləndi və qrupda paylaşıldı.")
        
    elif action == "decline_etiraf":
        await callback_query.message.edit_text("❌ Etiraf rədd edildi.")

# --- OYUNLAR VƏ MƏLUMAT SİSTEMİ ---
@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games_handler(client, message):
    icons = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    cmd = message.command[0]
    await client.send_dice(message.chat.id, icons.get(cmd, "🎲"))

@app.on_message(filters.command("id"))
async def get_id(client, message):
    user = message.from_user
    text = f"👤 **İstifadəçi:** {user.first_name}\n🆔 **ID:** `{user.id}`\n"
    if message.chat.type != ChatType.PRIVATE:
        text += f"👥 **Qrup ID:** `{message.chat.id}`"
    await message.reply_text(text)

@app.on_message(filters.command("info"))
async def user_info(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    status = await client.get_chat_member(message.chat.id, user.id)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT msg_count FROM user_stats WHERE user_id = %s", (user.id,))
    stats = cur.fetchone()
    msg_count = stats[0] if stats else 0
    cur.close(); conn.close()

    # 445-ci sətirdəki xətanın düzəldilmiş forması (Multi-line string)
    text = (
        f"📋 **İstifadəçi Məlumatı:**\n"
        f"• Ad: {user.first_name}\n"
        f"• ID: `{user.id}`\n"
        f"• Status: {status.status}\n"
        f"• Mesaj Sayı: {msg_count}"
    )
    await message.reply_text(text)

# --- BOTUN İŞƏ SALINMASI ---
async def main():
    async with app:
        load_plugins(app)
        
        # 467-ci sətir: set_bot_commands (hərf səhvini düzəltdim)
        await app.set_bot_commands([
            BotCommand("start", "Botu başladın"),
            BotCommand("help", "Kömək menyusu"),
            BotCommand("tag", "Brilyant tağ"),
            BotCommand("etiraf", "Anonim etiraf"),
            BotCommand("basket", "Basketbol"),
            BotCommand("futbol", "Futbol"),
            BotCommand("slot", "Kazino"),
            BotCommand("id", "ID göstər"),
            BotCommand("info", "Məlumat")
        ])
        
        print("🚀 Bot aktivdir və oyunlar yükləndi!")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    try:
        app.run(main())
    except KeyboardInterrupt:
        pass
