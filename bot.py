import os, asyncio, random, psycopg2
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}; chat_status = {}

# ----------------- 250+ BAYRAQLAR (HAMSİ BURDADIR) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬🇶","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼","🏴󠁧󠁢󠁥󠁮󠁧󠁿","🏴󠁧󠁢󠁳󠁣󠁴󠁿","🏴󠁧󠁢󠁷󠁬󠁳󠁿"]

# ----------------- 200+ EMOJİLƏR (HAMSİ BURDADIR) -----------------
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉","🎐","🎌","🚩","🏆","🎖️","🎫","💌","💍","Glasses","🎒","Hat","👟","👗","👑","Lipstick","Gloves","🧶","🧪","🧬","🔭","📡","💡","🕯️","📚","📕","📜","💵","💸","💳","⚖️","🗝️","🔓","🔨","🛡️","🏹","⚔️","💊","🩹","🩸","🧺","🧼","🧽","🪒","🚿","🛁","🧻","🧱","⛓️","🧨","🧧","🎀","🎊","🎐","🎋","🎎","🎏","🧠","齒","🦴","👀","👅","👄","👂","👃","👣","👁️‍🗨️","🗨️","🧣","🧥","👒","👜","👛","👗","👘","👖","👕","👞","👟"]

def get_db_connection(): return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(client, message):
    if message.chat.type == "private": return True
    try:
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        return user.status in ("administrator", "creator")
    except: return False

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = "sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ\nᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ.\nᴋᴏᴍᴜᴛʟᴀʀɪ öʏʀəɴᴍəᴋ üçüɴ /help ʏᴀᴢᴍᴀğıɴɪᴢ\nᴋɪғᴀʏəᴛᴅɪʀ."
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{app.get_me().username}?startgroup=true")],[InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]])
    await message.reply_text(text, reply_markup=markup)

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = "🎮 əʏʟəɴᴄəʟɪ ᴏʏᴜɴʟᴀʀ:\n\n🏀 /basket - ʙᴀsᴋᴇᴛʙᴏʟ\n⚽ /futbol - ғᴜᴛʙᴏʟ\n🎯 /dart - ᴅᴀʀᴛ\n🎰 /slot - sʟᴏᴛ\n🎲 /dice - ᴢᴀʀ\n\n📢 ᴛᴀğ ᴋᴏᴍᴀɴᴅᴀʟᴀʀɪ:\n🔹 /tag - ɴᴏʀᴍᴀʟ ᴛᴀğ\n🔹 /utag - ᴇᴍᴏᴊɪ ɪʟə ᴛᴀğ\n🔹 /flagtag - ʙᴀʏʀᴀǫʟᴀ ᴛᴀğ\n🔹 /tektag - ᴛəᴋ-ᴛəᴋ ᴛᴀğ\n\n🛑 ᴅᴀʏᴀɴᴅɪʀᴍᴀǫ üçüɴ: /stop\n💬 ᴄʜᴀᴛʙᴏᴛ: /chatbot on/off"
    await message.reply_text(text)

@app.on_message(filters.command("reload") & filters.group)
async def reload_cmd(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Bu komandanı yalnız adminlər istifadə edə bilər!")
    tag_process[message.chat.id] = False
    await message.reply_text("🔄 **Sistem yeniləndi!**")

@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def tag_handler(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Bu komandanı yalnız adminlər istifadə edə bilər!")
    chat_id = message.chat.id; tag_process[chat_id] = True; cmd = message.command[0].lower(); user_msg = " ".join(message.command[1:])
    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot and not m.user.is_deleted: members.append(m.user)
    for u in members:
        if not tag_process.get(chat_id, True): break
        if cmd == "flagtag": t = f"{user_msg} [{random.choice(BAYRAQLAR)}](tg://user?id={u.id})"
        elif cmd == "utag": t = f"{user_msg} [{random.choice(EMOJILER)}](tg://user?id={u.id})"
        elif cmd == "tektag": t = f"{user_msg} [{u.first_name}](tg://user?id={u.id})"
        else: t = f"{user_msg} [💎](tg://user?id={u.id})"
        try: await client.send_message(chat_id, t); await asyncio.sleep(2.0)
        except: pass
    tag_process[chat_id] = False

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Bu komandanı yalnız adminlər istifadə edə bilər!")
    tag_process[message.chat.id] = False; await message.reply_text("🛑 Tağ prosesi dayandırıldı!")

@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games_cmd(client, message):
    e = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    await client.send_dice(message.chat.id, emoji=e[message.command[0]])

@app.on_message(filters.command("chatbot") & filters.group)
async def cb_toggle(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Bu komandanı yalnız adminlər istifadə edə bilər!")
    if len(message.command) > 1: chat_status[message.chat.id] = (message.command[1].lower() == "on")
    await message.reply_text(f"✅ Chatbot {'aktiv' if chat_status.get(message.chat.id, True) else 'deaktiv'} edildi.")

@app.on_message(filters.group & ~filters.bot)
async def chatbot_logic(client, message):
    chat_id = message.chat.id
    try:
        conn = get_db_connection(); cur = conn.cursor()
        if message.text and not message.text.startswith('/'):
            if chat_status.get(chat_id, True) and random.random() < 0.20:
                cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
                res = cur.fetchone()
                if res: await message.reply_text(res[0])
            cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
            conn.commit()
        cur.close(); conn.close()
    except: pass

app.run()
