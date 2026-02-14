import os, asyncio, random, psycopg2
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus

# Ayarlar
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
OWNER_ID = 6241071228  # Sənin ID-n

app = Client("my_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
tag_process = {}; chat_status = {}

# Qısaldılmış Resurslar
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬🇶","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉","🎐","🎌","🚩","🏆","🎖️","🎫","💌","💍","👓","🎒","👒","👟","👗","👑","💄","🧤","🧶","🧪","🧬"," telescope","📡","💡","🕯️","📚","📕","📜","💵","💸","💳","⚖️","🗝️","🔓","🔨","🛡️","🏹","⚔️","💊","🩹","🩸","🧺","🧼","🧽","🪒","🚿","🛁","🧻","🧱","⛓️","🧨","🧧","🎀","🎊","🎐","🎋","🎎","🎏","🧠","🦷","🦴","👀","👅","👄","👂","👃","👣"]

def get_db(): return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(c, m):
    if m.chat.type.name == "PRIVATE" or (m.from_user and m.from_user.id == OWNER_ID): return True
    if m.sender_chat and m.sender_chat.id == m.chat.id: return True
    try:
        status = (await c.get_chat_member(m.chat.id, m.from_user.id)).status
        return status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"sᴀʟᴀᴍ! ᴛᴀɢ ᴠə əʏʟəɴᴄə ʙᴏᴛᴜʏᴀᴍ.\nᴋöᴍəᴋ üçüɴ /help ʏᴀᴢ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ əʟᴀᴠə ᴇᴛ", url=f"https://t.me/{(await c.get_me()).username}?startgroup=true")]]))

@app.on_message(filters.command("help"))
async def help(c, m):
    await m.reply_text("📢 /tag, /utag, /flagtag, /tektag\n🎮 /basket, /futbol, /dart, /slot, /dice\n🛑 /stop | 💬 /chatbot on/off")

@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
async def tagger(c, m):
    if not await is_admin(c, m): return await m.reply("❌ Admin deyilsən!")
    cid = m.chat.id
    tag_process[cid] = True
    cmd, txt = m.command[0], " ".join(m.command[1:])
    async for member in c.get_chat_members(cid):
        if not tag_process.get(cid) or member.user.is_bot: continue
        if cmd == "flagtag": t = f"{txt} {random.choice(BAYRAQLAR)}"
        elif cmd == "utag": t = f"{txt} {random.choice(EMOJILER)}"
        else: t = txt
        await c.send_message(cid, f"{t} [{member.user.first_name}](tg://user?id={member.user.id})")
        await asyncio.sleep(2)
    tag_process[cid] = False

@app.on_message(filters.command("stop") & filters.group)
async def stop(c, m):
    if await is_admin(c, m): tag_process[m.chat.id] = False; await m.reply("🛑 Dayandı.")

@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games(c, m):
    await c.send_dice(m.chat.id, emoji={"basket":"🏀","futbol":"⚽","dart":"🎯","slot":"🎰","dice":"🎲"}[m.command[0]])

@app.on_message(filters.command("chatbot") & filters.group)
async def chatbot(c, m):
    if await is_admin(c, m) and len(m.command) > 1:
        chat_status[m.chat.id] = (m.command[1] == "on")
        await m.reply(f"✅ Chatbot: {m.command[1]}")

@app.on_message(filters.group & ~filters.bot)
async def cb_logic(c, m):
    if not m.text or m.text.startswith('/'): return
    try:
        conn = get_db(); cur = conn.cursor()
        if chat_status.get(m.chat.id, True) and random.random() < 0.2:
            cur.execute("SELECT content FROM brain WHERE chat_id=%s ORDER BY RANDOM() LIMIT 1", (m.chat.id,))
            res = cur.fetchone()
            if res: await m.reply(res[0])
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (m.text, m.chat.id))
        conn.commit(); cur.close(); conn.close()
    except: pass

app.run()
