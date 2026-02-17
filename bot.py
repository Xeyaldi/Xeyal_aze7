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
TARGET_GROUP = "@sohbetqruprc"

# --- BOTLARIN QOŞULMASI ---
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

tag_process = {}

# --- SİYAHLAR (TOXUNULMADI) ---
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨CC","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎"," strawberry ","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]

# --- KÖMƏKÇİ FUNKSİYALAR ---
async def check_admin(client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in OWNERS: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

async def get_mention(client, user_input):
    try:
        user = await client.get_users(user_input)
        return f"[{user.first_name}](tg://user?id={user.id})"
    except: return f"`{user_input}`"

def get_rank(count):
    if count > 10000: return "💎 Marşal"
    if count > 5000: return "🌟 General"
    if count > 2000: return "🎖️ Polkovnik"
    if count > 1000: return "🎖️ Mayor"
    if count > 500: return "🎗️ Kapitan"
    if count > 200: return "💂 Leytenant"
    if count > 50: return "🔫 Çavuş"
    return "🛡️ Sıravi"

# --- START VƏ PANEL ---
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    buttons = [[InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
               [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
               [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]]
    await message.reply_photo(photo=SAKIL_LINKI, caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("back_home"))
async def back_home(client, callback_query):
    buttons = [[InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
               [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
               [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]]
    await callback_query.message.edit_caption(caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("⚠️ Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər", show_alert=True)
    await callback_query.message.edit_caption(caption="✨ **sᴀʜɪʙə ÖZƏL PANEL**\n\n📢 **Broadcast və digər ayarlar üçün /help yazın.**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri", callback_data="back_home")]]))

# --- TAĞ SİSTEMİ ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
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
                await client.send_message(message.chat.id, txt); await asyncio.sleep(2.5)
            except: pass

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await check_admin(client, message): return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

# --- MESAJ SAYĞACI VƏ KARMA ---
@app.on_message(filters.group & ~filters.bot, group=-1)
async def global_handler(client, message):
    c_id, u_id = message.chat.id, message.from_user.id
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (c_id, u_id))
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        if target_id != u_id:
            if message.text == "+":
                cur.execute("INSERT INTO user_karma (chat_id, user_id, karma_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET karma_count = user_karma.karma_count + 1", (c_id, target_id))
                await message.reply_text(f"➕ **{message.reply_to_message.from_user.first_name}** karması artdı!")
            elif message.text == "-":
                cur.execute("INSERT INTO user_karma (chat_id, user_id, karma_count) VALUES (%s, %s, -1) ON CONFLICT (chat_id, user_id) DO UPDATE SET karma_count = user_karma.karma_count - 1", (c_id, target_id))
                await message.reply_text(f"➖ **{message.reply_to_message.from_user.first_name}** karması azaldı!")
    conn.commit(); cur.close(); conn.close()

# --- TOPSİRALAMA VƏ REYTİNQ ---
@app.on_message(filters.command("topsiralama") & filters.group)
async def top_ranks(client, message):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT user_id, msg_count FROM user_stats WHERE chat_id = %s ORDER BY msg_count DESC LIMIT 20", (message.chat.id,))
    rows = cur.fetchall()
    if not rows: return await message.reply_text("🪖 Məlumat yoxdur.")
    text = "🎖️ **Qrupun Top 20 Aktiv Üzvü**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    for i, (u_id, count) in enumerate(rows, 1):
        mention = await get_mention(client, u_id); rank = get_rank(count)
        text += f"{i:02d}. {rank} | {mention}\n╰─ 💬 Mesaj: `{count}`\n\n"
    await message.reply_text(text); cur.close(); conn.close()

# --- TƏRCÜMƏ ---
@app.on_message(filters.command(["tercume", "traz", "tren", "trru", "trtr", "trde", "trfr"]))
async def multi_translate(client, message):
    if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
    text = message.reply_to_message.text or message.reply_to_message.caption
    if not text: return
    cmd = message.command[0].lower()
    target_lang = cmd[2:] if cmd != "tercume" else (message.command[1].lower() if len(message.command) > 1 else "az")
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
    try:
        res = requests.get(url).json()
        await message.reply_text(f"🌍 **Tərcümə ({target_lang.upper()}):**\n\n`{res[0][0][0]}`")
    except: await message.reply_text("❌ Xəta baş verdi.")

# --- DİGƏR KOMANDALAR (PDF, QR, WİKİ, OYUNLAR) ---
@app.on_message(filters.command("pdf"))
async def instant_pdf(client, message):
    if not message.reply_to_message: return await message.reply_text("❌ Reply verin!")
    target = message.reply_to_message
    photo_path = await target.download() if target.photo else None
    pdf_name = f"pdf_{message.from_user.id}.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    if photo_path:
        with Image.open(photo_path) as img: img.convert("L").save(photo_path)
        c.drawImage(photo_path, 50, 350, 500, 450); os.remove(photo_path)
    c.showPage(); c.save()
    await message.reply_document(pdf_name); os.remove(pdf_name)

@app.on_message(filters.command("qr"))
async def qr_cmd(client, message):
    if len(message.command) < 2: return
    txt = urllib.parse.quote(message.text.split(None, 1)[1])
    await message.reply_photo(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}")

@app.on_message(filters.command(["dice", "slot", "futbol", "basket"]))
async def games(client, message):
    em = {"dice":"🎲", "slot":"🎰", "futbol":"⚽", "basket":"🏀"}
    await client.send_dice(message.chat.id, emoji=em[message.command[0]])

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = "╔════════════════════╗\n   💠 **B O T  P R O  M E N Y U** 💠\n╚════════════════════╝\n\n🎖️ **REYТİNQ:** `/topsiralama`, `/topkarma`\n🌍 **TƏRCÜMƏ:** `/traz`, `/tren`, `/trru`\n📄 **MULTİMEDİA:** `/pdf`, `/qr`, `/wiki`\n🕹️ **ƏYLƏNCƏ:** `/love`, `/slap`, `/dice`\n💰 **MALİYYƏ:** `/kripto`, `/valyuta`\n🛠 **ADMİN:** `/purge`, `/id`, `/etiraf`\n"
    await message.reply_text(help_text)

# --- BROADCAST (YÖNLƏNDİR) ---
@app.on_message(filters.command("yonlendir") & filters.user(OWNERS))
async def broadcast_func(client, message):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("SELECT DISTINCT chat_id FROM user_stats"); chats = cur.fetchall()
    cur.close(); conn.close()
    for chat in chats:
        try:
            if message.reply_to_message: await message.reply_to_message.copy(chat[0])
            else: await client.send_message(chat[0], message.text.split(None, 1)[1])
            await asyncio.sleep(0.3)
        except: continue

# --- SKAN VƏ AUTO-JOIN ---
@app.on_message(filters.new_chat_members)
async def auto_join_and_scan(client, message):
    if any(m.is_self for m in message.new_chat_members):
        try:
            invite_link = await client.export_chat_invite_link(message.chat.id)
            if not user_app.is_connected: await user_app.start()
            await user_app.join_chat(invite_link)
            conn = get_db_connection(); cur = conn.cursor()
            async for msg in user_app.get_chat_history(message.chat.id, limit=None):
                if msg.from_user and not msg.from_user.is_bot:
                    cur.execute("INSERT INTO user_stats (chat_id, user_id, msg_count) VALUES (%s, %s, 1) ON CONFLICT (chat_id, user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (message.chat.id, msg.from_user.id))
            conn.commit(); cur.close(); conn.close()
        except: pass

# --- BOTU BAŞLATMAQ ---
async def start_bot():
    print("🚀 Bot başladılır...")
    await app.start()
    if SESSION_STRING:
        try: await user_app.start(); print("✅ Userbot aktivdir.")
        except: print("⚠️ Userbot qoşulmadı.")
    print("💎 Bot hər şeyi ilə tam hazırdır!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(start_bot())
