import os, asyncio, random, psycopg2
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Ayarlar
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
OWNER_ID = 6241071228 

SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}; chat_status = {}

# ----------------- 250+ BAYRAQLAR (KƏSİLMƏDİ) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧🇶","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬GQ","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮🇶","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲🇶","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱開","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼","🏴󠁧󠁢󠁥󠁮󠁧󠁿","🏴󠁧󠁢󠁳󠁣󠁴󠁿","🏴󠁧󠁢󠁷󠁬󠁳󠁿"]

# ----------------- 200+ EMOJİLƏR (KƏSİLMƏDİ) -----------------
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉","🎐","🎌","🚩","🏆","🎖️","🎫","💌","💍","👓","🎒","👒","👟","👗","👑","💄","🧤","🧶","🧪","🧬","伸縮","📡","💡","🕯️","📚","📕","📜","💵","💸","💳","⚖️","🗝️","🔓","🔨","🛡️","🏹","⚔️","💊","🩹","🩸","🧺","🧼","🧽","🪒","🚿","🛁","🧻","🧱","⛓️","🧨","🧧","🎀","🎊","🎐","🎋","🎎","🎏","🧠","🦷","🦴","👀","👅","👄","👂","👃","👣","👁️‍🗨️","🗨️","🧣","🧥","👒","👜","👛","👗","👘","👖","👕","👞","👟"]

# ----------------- 450+ HAZIR CHATBOT SÖZLƏRİ -----------------
CB_SOZLER = ["Salam","Necəsən?","Nə var nə yox?","Hardasan?","Xoş gəldin","Sağ ol","Buyur","Bəli","Xeyr","Əlbəttə","Can","Nolsun?","Gözəl","Bomba kimi","İşdəyəm","Evdəyəm","Yoldayam","Nə edirsən?","Heç nə","Boş-boş","Yaxşıyam çox sağ ol","Aleykum salam","Hər vaxtın xeyir","Gecən xeyrə","Sabahın xeyir","Görüşərik","Öpürəm","Ay can","Vay be","Oldu","Təşəkkür","Minatdaram","Zarafat eliyirsən?","Ciddi?","Hə də","Yox canım","Məncə də","Razıyam","Bilmirəm","Bəlkə","Sabah","Bu gün","Dünən","Nə zaman?","Kimləsən?","Təkəm","Dostlarla","Gəlirəm","Getdim","Hardasan sən?","Gözləyirəm","Tez ol","Gecikmə","İnanmırıam","Doğurdan?","Söz ola bilməz","Əla","Süper","Pis deyiləm","Yorulmuşam","Yatacam","Durmuşam","Çay içirəm","Yemək yeyirəm","Kofe lazımdı","Acımışam","Susuzam","Soyuqdur","İstidir","Külək var","Yağış yağır","Qar yağır","Darıxmışam","Gəl də","Gedək","Haraya?","Parka","Bulvara","Kino","Musiqi dinləyirəm","Hansı mahnı?","Maraqlıdır","Mənasızdır","Niyə belə?","Səbəb?","Nə bilim","Yadımdan çıxıb","Söz verdim","Gələcəm","Dəqiq?","Yüz faiz","Ehtiyatlı ol","Sakit ol","Əsəbləşmə","Gül biraz","Hahaha","Zor","Maraqlıdı","Nə deyim vallah","Baxarıq","İnşallah","Qismət","Nə qəşəng","Xeyirli olsun","Mübarəkdir","Təbriklər","Ad günün mübarək","Yaxşı ki varsan","Mən də həmçinin","Səni sevirəm","Canım","Həyatım","Ürəyim","Nəfəsim","Dünyam","Gözəlim","Şirinim","Acı","Turş","Şirin","Duzlu","Dadlıdır","Bəyəndim","Çox sağ ol","Yaxşılıqdır","Sən necəsən?","Hər şey qaydasındadır?","İşlər necə gedir?","Dərslər necədir?","İmtahan var?","Yoxdu","Bitdi","Başladı","Gözlə","Dayan","Keç","Gir","Çıx","Al","Ver","Yaz","Oxu","Danış","Sus","Bax","Gör","Eşit","Dinlə","Anla","Başa düşdüm","Anlamadım","Təkrar elə","Yenə?","Bəsdir","Yeter","Dostum","Qardaş","Bacı","Ana","Ata","Ailə","Vətən","Bakı","Azərbaycan","Gəncə","Sumqayıt","Naxçıvan","Qarabağ","Şuşa","Zəfər","Bayraq","Uğurlar","Maşallah","Bərəkallah","Amin","Dua elə","Unutma","Xatırla","Gözlərim","Saçım","Geyim","Moda","Telefon","Kompyuter","İnternet","Zəifdir","Güclüdür","Donur","İşləmir","Xarab olub","Düzələcək","Nə vaxt?","Heç vaxt","İndi","Tezliklə","Uzaq","Yaxın","Sağda","Solda","Düz","Əyri","Ağ","Qara","Qırmızı","Göy","Yaşıl","Sarı","Bənövşəyi","Narıncı","Boz","Qəhvəyi","Rəngli","Sadə","Bahalı","Ucuz","Pul","Maaş","Borç","Xərclə","Qazan","İtir","Tap","Axtar","Otur","Qaç","Yerində","Sakitçilik","Səs-küy","Musiqi","Səviyyə","Hörmət","Eşq","Nifrət","Qəzəb","Sevinc","Kədər","Göz Tears","Təbəssüm","Ümid","Arzu","Xəyal","Gələcək","Keçmiş","An","Zaman","Saat","Dəqiqə","Saniyə","Həftə","Ay","İl","Əsr","Bayram","Cümə","Şənbə","Bazar","Bazar ertəsi","Çərşənbə","Cümə axşamı","Həyat","Ömür","Dünya","Kainat","Ulduz","Ay","Günəş","Torpaq","Su","Hava","Od","Ruh","Bədən","Sağlamlıq","Xəstə","Həkim","Dərman","Yaxşı ol","Şəfa versin","Çox yaşa","Sən də gör","Xoşbəxt ol","Var ol","Yaşa","Yarat","Öyrən","Bil","Bacarıq","Zəka","Ağıl","Dəli","Ağıllı","Sakit","Dəcəl","Uşaq","Böyük","Gənc","Qoca","İnsan","Adam","Şəxsiyyət","Xarakter","Təbiət","Heyvan","Pişik","İt","Quş","Balıq","Dəniz","Okean","Göl","Çay","Meşə","Dağ","Düzənlik","Səhra","Cənnət","Cəhənnəm","Mələk","Şeytan","Xeyir","Şər","Yol","İz","Addım","Məsafə","Sərhəd","Azadlıq","Dustaq","Həbs","Məhkəmə","Qanun","Haqq","Ədalət","Zülm","Zəfər","Məğlubiyyət","Döyüş","Sülh","Əsgər","Vətəndaş","Millət","Xalq","Dövlət","Siyasət","İqtisadiyyat","Mədəniyyət","İncəsənət","Ədəbiyat","Şeir","Qəzəl","Mahnı","Rəqs","Rəsm","Heykəl","Memarlıq","Tarix","Coğrafiya","Riyaziyyat","Fizika","Kimya","Biologiya","Astronomiya","Məntiq","İnam","Şübhə","Qorxu","Cəsarət","Güç","Zəiflik","Zəfər","Məqsəd","Nəticə","Uğur","Uğursuzluq","Təcrübə","Səhv","Düz","Yalan","Həqiqət","Düzgünlük","Dürüstlük","Xəyanət","Vəfa","Sədaqət","Dostluq","Qardaşlıq","Məhəbbət","Sevgi","İlham","Yaradıcılıq","Həvəs","Maraq","Diqqət","Səbir","Dözüm","İradə","Ruh yüksəkliyi","İnamlı","Ümidsiz","Yalnız","Tənha","Kimsəsiz","Qərib","Müsafir","Qonaq","Süfrə","Çörək","Duz","Nemət","Bərəkət","Sübh","Axşam","Gecə","Gündüz","Günorta","Səhər","İstirahət","Yuxu","Röya","Gerçək","Xəyalpərəst","Məqsədyönlü","Çalışqan","Tənbəl","Zəhmətkeş","Dürüst","Yalançı","Xəsis","Səxavətli","Mərd","Namərd","Cavan","Yaşlı","Kişi","Qadın","Oğlan","Qız","Bala","Körpə","Nəvə","Nəticə","Kök","Nəsil","Şəcərə","Miras","Pay","Hissə","Bütün","Yarım","Dörddəbir","Faiz","Rəqəm","Ədəd","Sıfır","Bir","İki","Üç","Dörd","Beş","Altı","Yeddi","Səkkiz","Doqquz","On","Yüz","Min","Milyon","Milyard","Sonsuz","Sərhədsiz","Dərin","Dayaz","Geniş","Dar","Hündür","Alçaq","Ağır","Yüngül","Sərt","Yumşaq","İncə","Qalın","İsti","Soyuq","Ilıq","Təmiz","Çirkli","Yeni","Köhnə","Müasir","Qədim","Tez","Gec","Sürətli","Yavaş","Uca","Sakit","Aydın","Qaranlıq","Parlaq","Solğun","Dadlı","Dadsız","Gözəl","Çirkin","Xoş","Bəd","Xeyirli","Ziyanlı","Vacib","Lazımsız","Mümkün","İmkansız","Çətin","Asan","Mürəkkəb","Sadə","Gizli","Aşkar","Naməlum","Məlum","Yaxın","Uzaq","Əvvəl","Sonra","Həmişə","Heç vaxt","Bəzən","Tez-tez","Nadir","Daimi","Müvəqqəti"]

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

async def is_admin(client, message):
    if message.chat.type.name == "PRIVATE": return True
    if message.from_user and message.from_user.id == OWNER_ID: return True
    if message.sender_chat and message.sender_chat.id == message.chat.id: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    text = (
        "sᴀʟᴀᴍ ! ᴍəɴ ʜəᴍ ᴅᴀɴışᴀɴ, ʜəᴍ ᴅə ᴍüxᴛəʟɪғ\n"
        "ᴛᴀɢ əᴍʀʟəʀɪ ᴏʟᴀɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ʙᴏᴛᴀᴍ.\n"
        "ᴋᴏᴍᴜᴛʟᴀʀɪ öʏʀəɴᴍəᴋ üçüɴ /help ʏᴀᴢᴍᴀğıɴɪᴢ\n"
        "ᴋɪғᴀʏəᴛᴅɪʀ."
    )
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👩🏻‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 söʜʙəᴛ ǫʀᴜᴘᴜ", url="https://t.me/sohbetqruprc")]
    ])
    try:
        await client.send_photo(message.chat.id, photo=SAKIL_LINKI, caption=text, reply_markup=markup)
    except:
        await message.reply_text(text, reply_markup=markup)

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = (
        "🎮 əʏʟəɴᴄəʟɪ ᴏʏᴜɴʟᴀʀ:\n\n"
        "🏀 /basket - ʙᴀsᴋᴇᴛʙᴏʟ\n"
        "⚽ /futbol - ғᴜᴛʙᴏʟ\n"
        "🎯 /dart - ᴅᴀʀᴛ\n"
        "🎰 /slot - sʟᴏᴛ\n"
        "🎲 /dice - ᴢᴀʀ\n\n"
        "📢 ᴛᴀğ ᴋᴏᴍᴀɴᴅᴀʟᴀʀɪ:\n"
        "🔹 /tag - ɴᴏʀᴍᴀʟ ᴛᴀğ\n"
        "🔹 /utag - ᴇᴍᴏ]ɪ ɪʟə ᴛᴀğ\n"
        "🔹 /flagtag - ʙᴀʏʀᴀǫʟᴀ ᴛᴀğ\n"
        "🔹 /tektag - ᴛəᴋ-ᴛəᴋ ᴛᴀğ\n\n"
        "🛑 ᴅᴀʏᴀɴᴅɪʀᴍᴀǫ üçüɴ: /stop\n"
        "💬 ᴄʜᴀᴛʙᴏᴛ: /chatbot on/off"
    )
    await message.reply_text(text)

@app.on_message(filters.command("reload") & filters.group)
async def reload_cmd(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    tag_process[message.chat.id] = False
    await message.reply_text("🔄 Sistem yeniləndi!")

@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]) & filters.group)
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

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    tag_process[message.chat.id] = False
    await message.reply_text("🛑 Tağ prosesi dayandırıldı!")

@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games_cmd(client, message):
    e = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    await client.send_dice(message.chat.id, emoji=e[message.command[0]])

@app.on_message(filters.command("chatbot") & filters.group)
async def cb_toggle(client, message):
    if not await is_admin(client, message): return await message.reply_text("❌ Admin deyilsən!")
    if len(message.command) > 1:
        choice = message.command[1].lower()
        chat_status[message.chat.id] = (choice == "on")
        status_text = "Aktiv edildi ✅" if choice == "on" else "Deaktiv edildi 🛑"
        await message.reply_text(f"💬 Chatbot bu qrup üçün {status_text}")
    else:
        await message.reply_text("💬 Chatbotu idarə etmək üçün `/chatbot on` və ya `/chatbot off` yazın.")

@app.on_message(filters.group & ~filters.bot)
async def chatbot_logic(client, message):
    if not message.text or message.text.startswith('/'): return
    chat_id = message.chat.id
    msg_text = message.text.lower()
    bot_me = await client.get_me()
    
    if msg_text == "salam":
        return await message.reply_text("aleykum salam")
    
    if msg_text == "necəsən" or msg_text == "necesen":
        return await message.reply_text("pis bəs sən necəsə ?")
    
    if "xəyal" in msg_text or "xeyal" in msg_text:
        return await message.reply_text("istirahət elləmm")
    
    if bot_me.first_name.lower() in msg_text or f"@{bot_me.username.lower()}" in msg_text:
        return await message.reply_text("Bəli, buyur? Eşidirəm səni ✨")

    if not chat_status.get(chat_id, False): return

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 50% ehtimalla (daha tez-tez) cavab ver
        if random.random() < 0.50:
            cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
            res = cur.fetchone()
            reply = res[0] if res else random.choice(CB_SOZLER)
            await message.reply_text(reply)
        
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Chatbot xətası: {e}")

app.run()
