import telebot
import os
import psycopg2
import random
import time
from telebot import types

# Bot tənzimləmələri
TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
bot = telebot.TeleBot(TOKEN)

# Botun söhbət vəziyyəti (Default: ON)
chat_status = {}

# 250+ DÜNYA BAYRAQLARI
FLAGS = [
    "🇦🇿", "🇹🇷", "🇵🇰", "🇺🇿", "🇰🇿", "🇰🇬", "🇹🇲", "🇦🇱", "🇩🇿", "🇦🇸", "🇦🇩", "🇦🇴", "🇦🇮", "🇦🇶", "🇦🇬", "🇦🇷", "🇦🇲", "🇦🇼", "🇦🇺", "🇦🇹",
    "🇧🇸", "🇧🇭", "🇧🇩", "🇧🇧", "🇧🇪", "🇧🇿", "🇧🇯", "🇧🇲", "🇧🇹", "🇧🇴", "🇧🇦", "🇧🇼", "🇧🇷", "🇮🇴", "🇻🇬", "🇧🇳", "🇧🇬", "🇧🇫", "🇧🇮", "🇰🇭",
    "🇨🇲", "🇨🇦", "🇮🇨", "🇨🇻", "🇧🇶", "🇰🇾", "🇨🇫", "🇹🇩", "🇨🇱", "🇨🇳", "🇨🇽", "🇨🇨", "🇨🇴", "🇰🇲", "🇨🇬", "🇨🇩", "🇨🇰", "🇨🇷", "🇨🇮", "🇭🇷",
    "🇨🇺", "🇨🇼", "🇨🇾", "🇨🇿", "🇩🇰", "🇩🇯", "🇩🇲", "🇩🇴", "🇪🇨", "🇪🇬", "🇸🇻", "🇬🇶", "🇪🇷", "🇪🇪", "🇪🇹", "🇪🇺", "🇫🇰", "🇫🇴", "🇫🇯", "🇫🇮",
    "🇫🇷", "🇬🇫", "🇵🇫", "🇹🇫", "🇬🇦", "🇬🇲", "🇬🇪", "🇩🇪", "🇬🇭", "🇬🇮", "🇬🇷", "🇬🇱", "🇬🇩", "🇬🇵", "🇬🇺", "🇬🇹", "🇬🇬", "🇬🇳", "🇬🇼", "🇬🇾",
    "🇭🇹", "🇭🇳", "🇭🇰", "🇭🇺", "🇮🇸", "🇮🇳", "🇮🇩", "🇮🇷", "🇮🇶", "🇮🇪", "🇮🇲", "🇮🇱", "🇮🇹", "🇯🇲", "🇯🇵", "🇯🇪", "🇯🇴", "🇰🇪", "🇰🇮", "🇽🇰",
    "🇰🇼", "🇱🇦", "🇱🇻", "🇱🇧", "🇱🇸", "🇱🇷", "🇱🇾", "🇱🇮", "🇱🇹", "🇱🇺", "🇲🇴", "🇲🇰", "🇲🇬", "🇲🇼", "🇲🇾", "🇲🇻", "🇲🇱", "🇲🇹", "🇲🇭", "🇲🇶",
    "🇲🇷", "🇲🇺", "🇾🇹", "🇲🇽", "🇫🇲", "🇲🇩", "🇲🇨", "🇲🇳", "🇲🇪", "🇲🇸", "🇲🇦", "🇲🇿", "🇲🇲", "🇳🇦", "🇳🇷", "🇳🇵", "🇳🇱", "🇳🇨", "🇳🇿", "🇳🇮",
    "🇳🇪", "🇳🇬", "🇳🇺", "🇳🇫", "🇰🇵", "🇲🇵", "🇳🇴", "🇴🇲", "🇵🇦", "🇵🇬", "🇵🇾", "🇵🇪", "🇵🇭", "🇵🇳", "🇵🇱", "🇵🇹", "🇵🇷", "🇶🇦", "🇷🇪", "🇷🇴",
    "🇷🇺", "🇷🇼", "🇼🇸", "🇸🇲", "🇸🇹", "🇸🇦", "🇸🇳", "🇷🇸", "🇸🇨", "🇸🇱", "🇸🇬", "🇸🇽", "🇸🇰", "🇸🇮", "🇬🇸", "🇸🇧", "🇸🇴", "🇿🇦", "🇰🇷", "🇸🇸",
    "🇪🇸", "🇱🇰", "🇧🇱", "🇸🇭", "🇰🇳", "🇱🇨", "🇵🇲", "🇻🇨", "🇸🇩", "🇸🇷", "🇸🇿", "🇸🇪", "🇨🇭", "🇸🇾", "🇹🇼", "🇹🇯", "🇹🇿", "🇹🇭", "🇹🇱", "🇹🇬",
    "🇹🇰", "🇹🇴", "🇹🇹", "🇹🇳", "🇹🇲", "🇹🇨", "🇹🇻", "🇺🇬", "🇺🇦", "🇦🇪", "🇬🇧", "🇺🇸", "🇺🇾", "🇻🇮", "🇻🇺", "🇻🇦", "🇻🇪", "🇻🇳", "🇼🇫", "🇪🇭",
    "🇾🇪", "🇿🇲", "🇿🇼", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "🏴󠁧󠁢󠁷󠁬󠁳󠁿"
]

# 200+ RƏNGARƏNG EMOJİ (Adam emojisi yoxdur)
FANCY_EMOJIS = [
    "🌈", "🪐", "🎡", "🍭", "💎", "🔮", "⚡", "🔥", "🚀", "🛸", "🎈", "🎨", "🎭", "🎸", "👾", "🧪", "🧿", "🍀", "🍿", "🎁", 
    "🔋", "🧸", "🎉", "✨", "🌟", "🌙", "☀️", "☁️", "🌊", "🌋", "☄️", "🍄", "🌹", "🌸", "🌵", "🌴", "🍁", "🍎", "🍓", "🍍", 
    "🥥", "🍔", "🍕", "🍦", "🍩", "🥤", "🍺", "🚲", "🏎️", "🚁", "⛵", "🛰️", "📱", "💻", "💾", "📸", "🎥", "🏮", "🎬", 
    "🎧", "🎤", "🎹", "🎺", "🎻", "🎲", "🎯", "🎮", "🧩", "🦄", "🦁", "🦊", "🐼", "🐨", "🐯", "🐝", "🦋", "🦜", "🐬", 
    "🐳", "🐾", "🐉", "🎐", "🎌", "🚩", "🏆", "🎖️", "🎫", "💌", "💍", "👓", "🎒", "👒", "👟", "👗", "👑", "💄", "🧤", "💍", 
    "🧶", "🧪", "🧬", "🔭", "📡", "💡", "🕯️", "📚", "📕", "📜", "💵", "💸", "💳", "💎", "⚖️", "🗝️", "🔓", "🔨", "🛡️", "🏹", 
    "⚔️", "💊", "🩹", "🩸", "🧺", "🧼", "🧽", "🪒", "🚿", "🛁", "🧸", "🪞", "🧹", "🧺", "🧻", "🏮", "🧱", "⛓️", "🔭", "🩹", 
    "🧨", "🎈", "🧧", "🎀", "🎊", "🎐", "🎋", "🎎", "🎏", "🧠", "🦷", "🦴", "👀", "👅", "👄", "👂", "👃", "👣", "👁️‍🗨️", "🗨️", 
    "🧤", "🧣", "🧥", "👒", "👜", "👛", "👗", "👘", "👖", "👕", "👞", "👟", "👢", "👠", "👡", "🧤", "🧣", "🧶", "🧵", "🌑", "🌒", 
    "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌙", "🌚", "🌛", "🌜", "🌡️", "🌤️", "🌥️", "🌦️", "🌧️", "🌨️", "🌩️", "🌪️", "🌫️", "🌬️"
]

# 200+ HAZIR SÖHBƏT CAVABLARI
READY_RESPONSES = [
    "Necəsən?", "Nə edirsən?", "Səninlə söhbət etmək maraqlıdır.", "Mən hər şeyi yadda saxlayıram!", 
    "Sən çox ağıllısan.", "Buna inanmıram!", "Doğurdan?", "Bəli, tamamilə razıyam.", "Xeyr, mən belə düşünmürəm.",
    "Gəl başqa mövzudan danışaq.", "Mən bir süni intellektəm!", "Azərbaycan dilini çox sevirəm!", 
    "Qrupda maraqlı söhbətlər gedir.", "Dost olaq?", "Sənin adın çox qəşəngdir.", "Mən həmişə buradayam.",
    "Mənə bir sirr de.", "Səni izləyirəm 👀", "Gülməli bir şey de.", "Həyat maraqlıdır!", "Nə xəbər var?",
    "Bu gün çox yaraşıqlısan (və ya gözəlsən)!", "Məni kim yaradıb?", "Özünə yaxşı bax.", "Hər şey qaydasındadır?"
    # Qeyd: Bu siyahıya istədiyin 200 cümləni tək-tək vergüllə ayıra-ayıra əlavə edə bilərsən.
]

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# ----------------- START & MENYU -----------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_add = types.InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{bot.get_me().username}?startgroup=true")
    btn_dev = types.InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq")
    btn_channel = types.InlineKeyboardButton("💬söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")
    markup.add(btn_add)
    markup.add(btn_dev, btn_channel)
    about_text = "sᴀʟᴀᴍ ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ. ᴋᴏᴍᴜᴛʟᴀʀı öʏʀəɴᴍəᴋ üçüɴ /help ʏᴀᴢᴍᴀğıɴıᴢ ᴋɪғᴀʏəᴛᴅɪʀ."
    bot.send_message(message.chat.id, about_text, reply_markup=markup)

# ----------------- HELP -----------------
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
✨ ʙᴏᴛᴜɴ ᴋᴏᴍᴜᴛʟᴀʀɪ:
🔸 `/tektag [mesaj]` - Hər kəsi tək-tək yazdığın sözlə tağ edər.
🔸 `/utag` - 200+ emoji ilə rəngarəng tağ.
🔸 `/flagtag` - 250+ bayraqla dünya turu tağı.
🔸 `/tag [mesaj]` - 5-5 qruplaşdırıb tağ.
🔸 `/chatbot on/off` - Söhbəti aktiv/deaktiv et.
    """
    bot.reply_to(message, help_text, parse_mode="Markdown")

# ----------------- CHATBOT ON/OFF -----------------
@bot.message_handler(commands=['chatbot'])
def toggle_chat(message):
    chat_id = message.chat.id
    status = message.text.split()[-1].lower()
    if status == "on":
        chat_status[chat_id] = True
        bot.reply_to(message, "✅ **Chatbot Aktiv edildi!**")
    elif status == "off":
        chat_status[chat_id] = False
        bot.reply_to(message, "❌ **Chatbot Deaktiv edildi.**")

# ----------------- TAĞ MƏNTİQİ -----------------
def get_users(chat_id):
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT DISTINCT user_id, first_name FROM brain WHERE chat_id = %s", (chat_id,))
        users = cur.fetchall(); cur.close(); conn.close()
        return users
    except: return []

@bot.message_handler(commands=['tektag', 'utag', 'tag', 'flagtag'])
def tag_logic(message):
    chat_id = message.chat.id
    users = get_users(chat_id)
    if not users:
        bot.send_message(chat_id, "❌ **Hələ ki, tağ üçün kimsə qeydə alınmayıb.**")
        return

    cmd = message.text.split()[0].lower()
    user_msg = " ".join(message.text.split()[1:]) if len(message.text.split()) > 1 else ""

    if "tektag" in cmd:
        for uid, name in users:
            bot.send_message(chat_id, f"{user_msg} [{name}](tg://user?id={uid})", parse_mode="Markdown")
            time.sleep(0.5)
    elif "flagtag" in cmd:
        tag_text = "🌍 ᴅüɴʏᴀ ʙᴀʏʀᴀǫʟᴀʀɪ ᴛᴀɢɪ:\n\n"
        for uid, name in users:
            tag_text += f"{random.choice(FLAGS)} [{name}](tg://user?id={uid})  "
        bot.send_message(chat_id, tag_text, parse_mode="Markdown")
    elif "utag" in cmd:
        tag_text = "✨ **ʀəɴɢᴀʀəɴɢ ᴜɴɪᴠᴇʀsᴀʟ ᴛᴀɢ:**\n\n"
        for uid, name in users:
            e = random.sample(FANCY_EMOJIS, 2)
            tag_text += f"{e[0]} [{name}](tg://user?id={uid}) {e[1]} \n"
        bot.send_message(chat_id, tag_text, parse_mode="Markdown")
    elif "tag" in cmd:
        tag_text = f"📢 **{user_msg}**\n\n"
        for i, (uid, name) in enumerate(users):
            tag_text += f"{random.choice(FANCY_EMOJIS)} [{name}](tg://user?id={uid})  "
            if (i + 1) % 5 == 0:
                bot.send_message(chat_id, tag_text, parse_mode="Markdown")
                tag_text = ""
        if tag_text: bot.send_message(chat_id, tag_text, parse_mode="Markdown")

# ----------------- CHATBOT (ÖYRƏNMƏ VƏ DANIŞMA) -----------------
@bot.message_handler(content_types=['text', 'sticker', 'voice'])
def learn_and_speak(message):
    if message.text and message.text.startswith('/'): return
    conn = get_db_connection(); cur = conn.cursor()
    m_type = 'text' if message.text else 'sticker' if message.sticker else 'voice'
    f_id = message.sticker.file_id if message.sticker else message.voice.file_id if message.voice else None
    cur.execute("INSERT INTO brain (msg_type, content, file_id, chat_id, user_id, first_name) VALUES (%s,%s,%s,%s,%s,%s)",
                (m_type, message.text, f_id, message.chat.id, message.from_user.id, message.from_user.first_name))
    conn.commit()

    if chat_status.get(message.chat.id, True) and random.random() < 0.25:
        if random.choice(["ready", "learned"]) == "ready":
            bot.send_message(message.chat.id, random.choice(READY_RESPONSES))
        else:
            cur.execute("SELECT msg_type, content, file_id FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (message.chat.id,))
            res = cur.fetchone()
            if res:
                if res[0]=='text': bot.send_message(message.chat.id, res[1])
                elif res[0]=='sticker': bot.send_sticker(message.chat.id, res[2])
                elif res[0]=='voice': bot.send_voice(message.chat.id, res[2])
    cur.close(); conn.close()

bot.infinity_polling()
