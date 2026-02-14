import os, asyncio, random, psycopg2
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# Ayarlar
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
OWNER_ID = 6241071228 
SAHIBA_ID = 7592728364 

SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}; chat_status = {}

# ----------------- SİYAHILAR (DƏYİŞİLMƏDİ) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬GQ","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱開","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼","🏴󠁧󠁢󠁥󠁮󠁧󠁿","🏴󠁧󠁢󠁳󠁣󠁴󠁿","🏴󠁧󠁢󠁷󠁬󠁳󠁿"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉","🎐","🎌","🚩","🏆","🎖️","🎫","💌","💍","👓","🎒","👒","👟","👗","👑","💄","🧤","🧶","🧪","🧬","伸縮","📡","💡","🕯️","📚","📕","📜","💵","💸","💳","⚖️","🗝️","🔓","🔨","🛡️","🏹","⚔️","💊","🩹","🩸","🧺","🧼","🧽","🪒","🚿","🛁","🧻","磚","⛓️","🧨","🧧","🎀","🎊","🎐","🎋","🎎","🎏","🧠","🦷","🦴","👀","👅","👄","👂","👃","👣","👁️‍🗨️","🗨️","🧣","🧥","👒","👜","👛","👗","👘","👖","👕","👞","👟"]
CB_SOZLER = ["Salam","Necəsən?","Nə var nə yox?","Hardasan?","Xoş gəldin","Sağ ol","Buyur","Bəli","Xeyr","Əlbəttə","Can","Nolsun?","Gözəl","Bomba kimi","İşdəyəm","Evdəyəm","Yoldayam","Nə edirsən?","Heç nə","Boş-boş","Yaxşıyam çox sağ ol","Aleykum salam","Hər vaxtın xeyir","Gecən xeyrə","Sabahın xeyir","Görüşərik","Öpürəm","Ay can","Vay be","Oldu","Təşəkkür","Minatdaram","Zarafat eliyirsən?","Ciddi?","Hə də","Yox canım","Məncə də","Razıyam","Bilmirəm","Bəlkə","Sabah","Bu gün","Dünən","Nə zaman?","Kimləsən?","Təkəm","Dostlarla","Gəlirəm","Getdim","Hardasan sən?","Gözləyirəm","Tez ol","Gecikmə","İnanmırıam","Doğurdan?","Söz ola bilməz","Əla","Süper","Pis deyiləm","Yorulmuşam","Yatacam","Durmuşam","Çay içirəm","Yemək yeyirəm","Kofe lazımdı","Acımışam","Susuzam","Soyuqdur","İstidir","Külək var","Yağış yağır","Qar yağır","Darıxmışam","Gəl də","Gedək","Haraya?","Parka","Bulvara","Kino","Musiqi dinləyirəm","Hansı mahnı?","Maraqlıdır","Mənasızdır","Niyə belə?","Səbəb?","Nə bilim","Yadımdan çıxıb","Söz verdim","Gələcəm","Dəqiq?","Yüz faiz","Ehtiyatlı ol","Sakit ol","Əsəbləşmə","Gül biraz","Hahaha","Zor","Maraqlıdı","Nə bilim vallah","Baxarıq","İnşallah","Qismət","Nə qəşəng","Xeyirli olsun","Mübarəkdir","Təbriklər","Ad günün mübarək","Yaxşı ki varsan","Mən də həmçinin","Səni sevirəm","Canım","Həyatım","Ürəyim","Nəfəsim","Dünyam","Gözəlim","Şirinim","Acı","Turş","Şirin","Duzlu","Dadlıdır","Bəyəndim","Çox sağ ol","Yaxşılıqdır"]

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(client, message):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in [OWNER_ID, SAHIBA_ID]: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await client.set_bot_commands([
        BotCommand("start", "Botu başladın"),
        BotCommand("help", "Kömək menyusu"),
        BotCommand("id", "ID göstərər"),
        BotCommand("tag", "Hamını tağ et"),
        BotCommand("utag", "Emoji ilə tağ"),
        BotCommand("flagtag", "Bayraqla tağ"),
        BotCommand("tektag", "Tək-tək tağ"),
        BotCommand("tagstop", "Tağı dayandır"),
        BotCommand("chatbot", "Chatbot on/off")
    ])
    
    user_id = message.from_user.id
    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]
    ]
    
    if user_id in [OWNER_ID, SAHIBA_ID]:
        buttons.append([InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")])

    text = (
        "sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ\n"
        "ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ.\n"
        "ᴋᴏᴍᴜᴛʟᴀʀɪ öʏʀəɴᴍəᴋ üçüɴ /help ʏᴀᴢᴍᴀğıɴɪᴢ\n"
        "ᴋɪғᴀʏəᴛᴅɪʀ."
    )
    markup = InlineKeyboardMarkup(buttons)
    try:
        await client.send_photo(message.chat.id, photo=SAKIL_LINKI, caption=text, reply_markup=markup)
    except:
        await message.reply_text(text, reply_markup=markup)

@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag", "tagstop", "chatbot"]))
async def group_check(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ Bu komanda yalnız qruplar üçündür!")
    
    # Komandaları yönləndir
    cmd = message.command[0].lower()
    if cmd in ["tag", "utag", "flagtag", "tektag"]: await tag_handler(client, message)
    elif cmd == "tagstop": await tagstop_cmd(client, message)
    elif cmd == "chatbot": await cb_toggle(client, message)

async def tag_handler(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0].lower()
    user_msg = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    members = []
    async for m in client.get_chat_members(chat_id):
        if m.user and not m.user.is_bot and not m.user.is_deleted:
            members.append(m.user)
    
    for u in members:
        if not tag_process.get(chat_id, False): break
        if cmd == "flagtag": t = f"{user_msg} {random.choice(BAYRAQLAR)} [{u.first_name}](tg://user?id={u.id})"
        elif cmd == "utag": t = f"{user_msg} {random.choice(EMOJILER)} [{u.first_name}](tg://user?id={u.id})"
        elif cmd == "tektag": t = f"{user_msg} [{u.first_name}](tg://user?id={u.id})"
        else: t = f"{user_msg} 💎 [{u.first_name}](tg://user?id={u.id})"
        try:
            await client.send_message(chat_id, t)
            await asyncio.sleep(2.5)
        except: pass
    tag_process[chat_id] = False

async def tagstop_cmd(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    tag_process[message.chat.id] = False
    await message.reply_text("🛑 Tağ dayandırıldı!")

async def cb_toggle(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    if len(message.command) > 1:
        choice = message.command[1].lower()
        if choice in ["on", "off"]:
            chat_status[message.chat.id] = (choice == "on")
            await message.reply_text(f"💬 Chatbot **{choice}** edildi.")
        else:
            await message.reply_text("Zəhmət olmasa `/chatbot on` və ya `/chatbot off` yazın.")
    else:
        await message.reply_text("İdarə üçün: `/chatbot on/off`")

@app.on_message(filters.command("id"))
async def id_show(client, message):
    await message.reply_text(f"🆔 **Sənin ID:** `{message.from_user.id}`\n📍 Çat ID: `{message.chat.id}`")

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = (
        "🎮 əʏʟəɴᴄəʟɪ ᴏʏᴜɴʟᴀʀ: /basket, /futbol, /dart, /slot, /dice\n\n"
        "📢 ᴛᴀğ ᴋᴏᴍᴀɴᴅᴀʟᴀʀɪ:\n/tag, /utag, /flagtag, /tektag\n\n"
        "🛑 ᴅᴀʏᴀɴᴅɪʀᴍᴀǫ: /tagstop\n"
        "💬 ᴄʜᴀᴛʙᴏᴛ: /chatbot on/off\n"
        "🆔 ID öʏʀəɴᴍəᴋ: /id"
    )
    await message.reply_text(text)

@app.on_message(filters.command("yonlendir") & filters.user([OWNER_ID, SAHIBA_ID]))
async def yonlendir_cmd(client, message):
    if len(message.command) < 2: return await message.reply_text("Mesaj yazın.")
    await message.reply_text("📢 Yönləndirmə aktivdir.")

@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in [OWNER_ID, SAHIBA_ID]:
        return await callback_query.answer("Bu komut sadəcə sahibə üçündür!", show_alert=True)
    await callback_query.edit_message_caption(
        caption="✨ Sahibə Paneli\n\nKomanda: `/yonlendir [mesaj]`", 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 ʏöɴʟəɴᴅɪʀ", callback_data="yonlendir_btn")]])
    )

@app.on_message(filters.group & ~filters.bot)
async def chatbot_logic(client, message):
    if not message.text or message.text.startswith('/'): return
    chat_id = message.chat.id
    msg_text = message.text.lower()
    bot_me = await client.get_me()
    if bot_me.first_name.lower() in msg_text or f"@{bot_me.username.lower()}" in msg_text:
        return await message.reply_text("Bəli, buyur? ✨")
    if not chat_status.get(chat_id, False): return
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if random.random() < 0.50:
            cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
            res = cur.fetchone()
            reply = res[0] if res else random.choice(CB_SOZLER)
            await message.reply_text(reply)
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
        conn.commit()
        cur.close(); conn.close()
    except: pass

app.run()
