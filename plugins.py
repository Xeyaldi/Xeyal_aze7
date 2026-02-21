from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import asyncio

# --- MAŞINLAR MENYUSU (12 MAŞIN) ---
@app.on_message(filters.command("masinlar"))
async def masin_menyu(client, message):
    buttons = [
        [InlineKeyboardButton("🏎️ Ferrari", callback_data="car_ferrari"),
         InlineKeyboardButton("🐃 Lamborghini", callback_data="car_lambo")],
        [InlineKeyboardButton("🌀 BMW", callback_data="car_bmw"),
         InlineKeyboardButton("⭐️ Mercedes", callback_data="car_merc")],
        [InlineKeyboardButton("🐎 Porsche", callback_data="car_porsche"),
         InlineKeyboardButton("💍 Audi", callback_data="car_audi")],
        [InlineKeyboardButton("⚡ Tesla", callback_data="car_tesla"),
         InlineKeyboardButton("🇯🇵 Toyota", callback_data="car_toyota")],
        [InlineKeyboardButton("💎 Bugatti", callback_data="car_bugatti"),
         InlineKeyboardButton("🐉 Nissan", callback_data="car_nissan")],
        [InlineKeyboardButton("👑 Rolls-Royce", callback_data="car_rolls"),
         InlineKeyboardButton("🧡 McLaren", callback_data="car_mclaren")]
    ]
    await message.reply_text(
        "**╔════════════════════╗**\n"
        "** 🚗 PREMİUM AVTO KATALOQ    **\n"
        "**╚════════════════════╝**\n\n"
        "✨ *Dünyanın ən məşhur 12 brendi haqqında ətraflı məlumat üçün seçiminizi edin:*",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- MƏLUMATLAR VƏ DETALLI EFFEKTLƏR ---
@app.on_callback_query(filters.regex("^car_"))
async def car_info(client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1]
    
    if data == "back":
        # Əsas menyuya qayıdış (12 butonlu)
        buttons = [
            [InlineKeyboardButton("🏎️ Ferrari", callback_data="car_ferrari"), InlineKeyboardButton("🐃 Lamborghini", callback_data="car_lambo")],
            [InlineKeyboardButton("🌀 BMW", callback_data="car_bmw"), InlineKeyboardButton("⭐️ Mercedes", callback_data="car_merc")],
            [InlineKeyboardButton("🐎 Porsche", callback_data="car_porsche"), InlineKeyboardButton("💍 Audi", callback_data="car_audi")],
            [InlineKeyboardButton("⚡ Tesla", callback_data="car_tesla"), InlineKeyboardButton("🇯🇵 Toyota", callback_data="car_toyota")],
            [InlineKeyboardButton("💎 Bugatti", callback_data="car_bugatti"), InlineKeyboardButton("🐉 Nissan", callback_data="car_nissan")],
            [InlineKeyboardButton("👑 Rolls-Royce", callback_data="car_rolls"), InlineKeyboardButton("🧡 McLaren", callback_data="car_mclaren")]
        ]
        return await callback_query.edit_message_text(
            "**🚗 MAŞIN KATALOQU**\n\n✨ *Yenidən seçim edin:*",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    infos = {
        "ferrari": (
            "**🏎️ FERRARI (İtaliya)**\n\n"
            "● **Təsisçi:** Enzo Ferrari (1939)\n"
            "● **Xüsusiyyəti:** Yarış dünyasının (Formula 1) kralı sayılır. Qırmızı rəngi və 'Şahə qalxmış at' loqosu ilə tanınır.\n"
            "● **Performans:** Sürət, lüks və aerodinamikanın zirvəsidir. Hər bir Ferrari mühərriki bir musiqi aləti kimi xüsusi səslənmə üçün tənzimlənir."
        ),
        "lambo": (
            "**🐃 LAMBORGHINI (İtaliya)**\n\n"
            "● **Təsisçi:** Ferruccio Lamborghini (1963)\n"
            "● **Xüsusiyyəti:** Aqressiv dizaynı və kəskin xətləri ilə tanınır. Loqosundakı qəzəbli buğa gücün və dözümlülüyün rəmzidir.\n"
            "● **Detallar:** 'Aventador' və 'Huracan' kimi modelləri ilə dünyanı fəth edib. Qapılarının yuxarı açılması (Lambo-doors) brendin vizit kartıdır."
        ),
        "bmw": (
            "**🌀 BMW (Almaniya)**\n\n"
            "● **Məna:** Bayerische Motoren Werke.\n"
            "● **Şüar:** 'Sürmə həzzi' (Sheer Driving Pleasure).\n"
            "● **Xüsusiyyəti:** Arxa çəkişli balansı və sürücüyə fokuslanmış daxili dizaynı ilə məşhurdur. M seriyası dünyada ən çox sevilən idman sedanlarıdır."
        ),
        "merc": (
            "**⭐️ MERCEDES-BENZ (Almaniya)**\n\n"
            "● **Şüar:** 'The Best or Nothing' (Ya ən yaxşısı, ya da heç nə).\n"
            "● **Liderlik:** Lüksün və təhlükəsizliyin pioneridir. İlk daxili yanma mühərrikli maşını bu brend yaradıb.\n"
            "● **Status:** S-Class dünyada dövlət başçılarının və biznesmenlərin ən çox üstünlük verdiyi lüks avtomobildir."
        ),
        "porsche": (
            "**🐎 PORSCHE (Almaniya)**\n\n"
            "● **Daimilik:** 911 modeli 50 ildən çoxdur ki, dizaynını köklü dəyişmədən mükəmməlləşdirilir.\n"
            "● **Xüsusiyyəti:** Gündəlik şəhər sürüşünə tam uyğun olan yeganə superkardır.\n"
            "● **Mühəndislik:** Mühərrikin arxada olması onlara unikal bir yol tutuşu və stabil sürətlənmə verir."
        ),
        "audi": (
            "**💍 AUDI (Almaniya)**\n\n"
            "● **Texnologiya:** 'Quattro' (4x4) sistemi ilə ralli dünyasında inqilab edib. Bütün hava şəraitlərində ən yaxşı yol tutuşu Audidədir.\n"
            "● **Dizayn:** Matrix LED işıqları və minimalist 'Virtual Cockpit' daxili dizaynı ilə texnoloji liderlik edir."
        ),
        "tesla": (
            "**⚡ TESLA (ABŞ)**\n\n"
            "● **Gələcək:** Dünyanı tam elektrikli nəqliyyata keçirməkdə liderdir.\n"
            "● **Güc:** Plaid modelləri 0-100 km/saat sürəti 2 saniyədən daha az müddətdə yığır.\n"
            "● **Texnologiya:** Maşın deyil, sanki təkərli bir kompyuterdir; avtopilot və sonsuz yenilənmə dəstəyi var."
        ),
        "toyota": (
            "**🇯🇵 TOYOTA (Yaponiya)**\n\n"
            "● **Etibarlılıq:** Dünyanın ən dözümlü və ən çox satılan maşınlarıdır.\n"
            "● **Statistika:** Corolla modeli tarixin ən çox satılan avtomobili ünvanını daşıyır.\n"
            "● **Hibrid:** Dünyada hibrid texnologiyasını kütləviləşdirən brenddir, yanacaq qənaətində rəqib tanımır."
        ),
        "bugatti": (
            "**💎 BUGATTI (Fransa)**\n\n"
            "● **Mükəmməllik:** Dünyanın ən baha, ən sürətli və ən güclü seriya maşınları.\n"
            "● **Rəqəmlər:** 1500+ at gücü və 16 silindrli (W16) mühərrik. Maksimum sürəti 400 km/saatdan çoxdur.\n"
            "● **Eksklüziv:** Hər bir Bugatti tək-tək əllə yığılır və sənət əsəri hesab olunur."
        ),
        "nissan": (
            "**🐉 NISSAN (Yaponiya)**\n\n"
            "● **Əfsanə:** 'Godzilla' ləqəbli Nissan GT-R modeli superkarları utandıran performansı ilə məşhurdur.\n"
            "● **Mədəniyyət:** JDM (Yaponiya daxili bazarı) tuning dünyasının bir nömrəli brendidir.\n"
            "● **Performans:** Sürəti və drift qabiliyyəti ilə yarış həvəskarlarının idealıdır."
        ),
        "rolls": (
            "**👑 ROLLS-ROYCE (Böyük Britaniya)**\n\n"
            "● **Aristokratiya:** Dünyanın ən lüks və ən bahalı sedanlarını istehsal edir.\n"
            "● **Səssizlik:** Salonda o qədər səssizlikdir ki, yalnız saatin çıqqıltısını eşitmək olar.\n"
            "● **Özəllik:** 'Spirit of Ecstasy' fiquru və tavandakı ulduzlu göy üzü işıqlandırması brendin simvoludur."
        ),
        "mclaren": (
            "**🧡 MCLAREN (Böyük Britaniya)**\n\n"
            "● **Yarış Ruhu:** Formula 1 texnologiyalarını birbaşa küçə maşınlarına tətbiq edən brenddir.\n"
            "● **Xüsusiyyəti:** Tamamilə karbon lifindən hazırlanmış şassi sayəsində inanılmaz dərəcədə yüngül və çevikdir.\n"
            "● **Dizayn:** Havalandırma kanalları və futuristik görünüşü ilə gələcəyin maşını təsirini bağışlayır."
        )
    }
    
    await callback_query.answer("Məlumat yükləndi...") 
    await callback_query.edit_message_text(
        infos.get(data, "Məlumat tapılmadı."),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri qayıt", callback_data="car_back")]])
    )

# --- ŞRİFTLƏRİN LÜĞƏTİ (Dəyişməz hissə) ---
FONTS = {
    "f1": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫", 
    "f2": "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃", 
    "f3": "𝔞𝔟ℭ𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷", 
    "f4": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ", 
    "f5": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ", 
    "f7": "αႦƈԃҽϝɠԦιʝƙʅɱɳσρϙɾʂƚυʋɯϰყȥ", 
    "f8": "ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչ", 
    "f9": "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐗ山乂ㄚ乙", 
    "f10": "A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶", 
    "f12": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉", 
    "f13": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉"
}

NORMAL_CHARS = "abcdefghijklmnopqrstuvwxyz"

def font_converter(text, font_type):
    if font_type == "f6": # Güzgü effekti
        return text[::-1]
    
    result = ""
    font_alphabet = FONTS.get(font_type)
    for char in text.lower():
        if char in NORMAL_CHARS:
            index = NORMAL_CHARS.index(char)
            result += font_alphabet[index]
        else:
            result += char
    return result

# --- ŞRİFT KOMANDASI ---
@app.on_message(filters.command("font"))
async def font_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Zəhmət olmasa mətni yazın.**\nMəsələn: `/font Salam`")
    
    user_text = " ".join(message.command[1:])
    
    # Düymələri 13 şriftə tamalayırıq
    buttons = [
        [InlineKeyboardButton("𝔻𝕠𝕦𝕓𝕝𝕖", callback_data=f"fn_f1"),
         InlineKeyboardButton("𝓢𝓬𝓻𝓲𝓹𝓽", callback_data=f"fn_f2")],
        [InlineKeyboardButton("𝔉𝔯𝔞𝔨𝔱𝔲𝔯", callback_data=f"fn_f3"),
         InlineKeyboardButton("Ⓒⓘⓡⓒⓛⓔⓓ", callback_data=f"fn_f4")],
        [InlineKeyboardButton("sᴍᴀʟʟ ᴄᴀᴘs", callback_data=f"fn_f5"),
         InlineKeyboardButton("Inverted", callback_data=f"fn_f6")],
        [InlineKeyboardButton("Gɾҽҽƙ", callback_data=f"fn_f7"),
         InlineKeyboardButton("คɭเєภ", callback_data=f"fn_f8")],
        [InlineKeyboardButton("卂丂丨卂几", callback_data=f"fn_f9"),
         InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data=f"fn_f10")],
        [InlineKeyboardButton("🅂🅀🅄🄰🅁🄴", callback_data=f"fn_f12"),
         InlineKeyboardButton("🅰🅱🅲", callback_data=f"fn_f13")],
        [InlineKeyboardButton("🎨 Qarışıq Stil", callback_data="fn_f1")]
    ]
    
    await message.reply_text(
        f"**╔════════════════════╗**\n"
        f"** 📝 ŞRİFT DEYİŞDİRİCİ      **\n"
        f"**╚════════════════════╝**\n\n"
        f"🔡 **Mətniniz:** `{user_text}`\n\n"
        f"✨ *Aşağıdakı 13 stildən birini seçin:*",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- CALLBACK (Şrift üçün) ---
@app.on_callback_query(filters.regex("^fn_"))
async def font_callback(client, callback_query: CallbackQuery):
    font_id = callback_query.data.split("_")[1]
    
    # Orijinal mətni mesajdan çəkirik
    try:
        original_text = callback_query.message.text.split("`")[1]
    except:
        return await callback_query.answer("❌ Mətn tapılmadı.")
    
    converted_text = font_converter(original_text, font_id)
    
    await callback_query.edit_message_text(
        f"✨ **Yeni şriftlə mətniniz:**\n\n"
        f"`{converted_text}`\n\n"
        f"👆 *Kopyalamaq üçün üstünə basın.*",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri qayıt", callback_data="car_back")]])
    )

# --- 💖 SEVGİ LABORATORİYASI (ULTRA ELİTE V4) ---
@app.on_message(filters.command("sevgi") & filters.group)
async def love_ultra_elite(client, message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: target = await client.get_users(message.command[1])
        except: return await message.reply_text("❌ **İstifadəçi tapılmadı!**")
    else:
        return await message.reply_text("💖 **Analiz üçün birinə reply atın və ya adını yazın.**")

    if target.id == message.from_user.id:
        return await message.reply_text("😅 **Özünə eşq elan etmək? Gəl bir az ciddi olaq...**")

    status = await message.reply_text("🧪 **Qan qrupları yoxlanılır...**")
    await asyncio.sleep(0.5)
    await status.edit_text("🛰 **Kosmik enerji xəritəsi çəkilir...**")
    await asyncio.sleep(0.5)
    await status.edit_text("🧬 **Ruh əkizi ehtimalı hesablanır...**")
    await asyncio.sleep(0.5)

    p = random.randint(0, 100)
    ehtiras = random.randint(10, 100)
    sadiqlik = random.randint(10, 100)
    bar = "❤️" * (p // 10) + "🖤" * (10 - (p // 10))

    if p == 0: res, msg = "☢️ TOKSİK", "Bir-birinizdən qaçın! Atom bombası qədər təhlükəlidir."
    elif 1 <= p <= 15: res, msg = "🧊 SİBİR", "Hisslər tamamilə donub, heç bir ümid yoxdur."
    elif 16 <= p <= 30: res, msg = "🧱 DİVAR", "Ünsiyyət sıfıra bərabərdir, sanki fərqli dildəsiniz."
    elif 31 <= p <= 45: res, msg = "☕ QEYBƏT", "Yaxşı çay və qeybət dostu ola bilərsiniz."
    elif 46 <= p <= 60: res, msg = "☁️ DUMANLI", "Hələ ki hər şey qeyri-müəyyəndir, gözləyin."
    elif 61 <= p <= 75: res, msg = "🔥 ALOVLU", "Hisslər isinir! İlk addımı mütləq kimsə atmalıdır."
    elif 76 <= p <= 85: res, msg = "🌋 VULKAN", "Ehtiras partlayışı! Qrupda yanğın söndürən lazımdır."
    elif 86 <= p <= 95: res, msg = "💎 BRİLYANT", "Nadir tapılan bir uyğunluq, itirməyin!"
    elif 96 <= p <= 99: res, msg = "👑 KRAL VƏ XATUN", "Siz sanki nağıllardan çıxmısınız. Maşallah!"
    else: res, msg = "💍 ƏSRİN EŞQİ", "Tarix sizi Leyli və Məcnun kimi tanıyacaq! 💖"

    final = (
        f"**╔════════════════════╗**\n"
        f"** ❤️ SEVGİ HESABATI (V4)    **\n"
        f"**╚════════════════════╝**\n\n"
        f"👤 **Aşiq:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
        f"👤 **Məşuq:** [{target.first_name}](tg://user?id={target.id})\n\n"
        f"📊 **Ümumi Uyğunluq:** `{p}%` \n"
        f"**[{bar}]**\n\n"
        f"🔥 **Ehtiras:** `{ehtiras}%` | ✅ **Sadiqlik:** `{sadiqlik}%` \n\n"
        f"📌 **Status:** `{res}`\n"
        f"💬 **Botun Rəyi:** _{msg}_"
    )
    await status.edit_text(final)

# --- 👊 ŞAPALAQ (SLAP MEGA PACK - 25+ VARIANT) ---
@app.on_message(filters.command("slap") & filters.group)
async def slap_mega_pack(client, message):
    if message.reply_to_message:
        t_user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: t_user = await client.get_users(message.command[1])
        except: return
    else: return await message.reply_text("👊 **Kimi vuraq?** Reply atın.")

    me = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    him = f"[{t_user.first_name}](tg://user?id={t_user.id})"

    slaps = [
        f"🧤 {me}, {him} şəxsini **Osmanlı şilləsi** ilə yerə sərdi!",
        f"👟 {me}, {him} üzünə **45 razmer yaş krossovka** tulladı!",
        f"🐟 {me}, {him} şəxsini **Xəzər nərəsi** ilə döydü!",
        f"🛋 {me}, {him} şəxsinə **qonaq otağının divanını** tulladı!",
        f"🧹 {me}, {him} şəxsini **süpürgə ilə** qovdu!",
        f"🚜 {me}, {him} şəxsinin üstündən **traktorla** keçdi!",
        f"🛸 {me}, {him} şəxsini **Marsa** fırlatdı!",
        f"🍳 {me}, {him} başına **isti tava** ilə vurdu (DANNG!)",
        f"🌵 {me}, {him} şəxsini **kaktus kolunun** üstünə oturtdu!",
        f"🥊 {me}, {him} şəxsinə **Mayk Tayson** zərbəsi vurdu!",
        f"🚀 {me}, {him} şəxsini **raketlə** Aya göndərdi!",
        f"🚗 {me}, {him} şəxsini **Priusla** vurdu!",
        f"🥄 {me}, {him} şəxsini **çay qaşığı** ilə döydü!",
        f"🎭 {me}, {him} şəxsinə **elə bir şillə vurdu ki**, uşaq kim olduğunu unutdu!",
        f"🧱 {me}, {him} şəxsinə **virtual kərpic** atdı!",
        f"🍗 {me}, {him} üzünə **toyuq budu** ilə vurdu!",
        f"💥 {me}, {him} şəxsini **yerlə yeksan etdi!**",
        f"🧊 {me}, {him} köynəyinə **bir vedrə buz** boşaltdı!",
        f"🦖 {me}, {him} üstünə **ac bir T-Rex** buraxdı!",
        f"🌪 {me}, {him} şəxsini **tornado** ilə uçurub apardı!",
        f"🥘 {me}, {him} başına **qazanla** vurdu!",
        f"🪓 {me}, {him} şəxsini **balta** (virtual) ilə qorxutdu!",
        f"🚿 {me}, {him} şəxsini **soyuq duşun** altına saldı!",
        f"🎈 {me}, {him} şəxsini **hava şarı** ilə göyə uçurtdu!",
        f"🚁 {me}, {him} şəxsini **helikopterin pərindən** asdı!",
        f"🎱 {me}, {him} şəxsinə **bilyard şarı** atdı!"
    ]
    await message.reply_text(random.choice(slaps))

# --- 🧠 ZEKA ÖLÇƏN (IQ TEST PRO) ---
@app.on_message(filters.command("zeka") & filters.group)
async def zeka_olcen(client, message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: target = await client.get_users(message.command[1])
        except: return await message.reply_text("❌ **İstifadəçi tapılmadı!**")
    else:
        return await message.reply_text("🧠 **Kimin zəkasını ölçmək istəyirsiniz?**\nReply atın və ya `/zeka @user` yazın.")

    # Analiz animasiyası
    status = await message.reply_text("🌀 **Beyin dalğaları skan edilir...**")
    await asyncio.sleep(0.7)
    await status.edit_text("🧪 **Məntiq hüceyrələri analiz olunur...**")
    await asyncio.sleep(0.7)
    await status.edit_text("📊 **Neyron bağlantıları yoxlanılır...**")
    await asyncio.sleep(0.7)

    iq = random.randint(30, 200) # IQ aralığı
    
    # IQ səviyyəsinə görə rəngli və zəngin şərhlər
    if iq <= 50:
        res, comment = "🥔 Kartof Zəkası", "Beyin yerinə kartof daşıyırsan? Bir az kitab oxu!"
    elif 51 <= iq <= 75:
        res, comment = "💡 Zəif İşiq", "Məntiqlə aran çox da yaxşı deyil, amma yaşayırsan da..."
    elif 76 <= iq <= 90:
        res, comment = "📉 Orta-Aşağı", "Hələ ki, standart bir insansan. Bir az öz üzərində işlə."
    elif 91 <= iq <= 110:
        res, comment = "⚖️ Normal Zəka", "Təbriklər! Dünyanın əksər faizi ilə eyni səviyyədəsən."
    elif 111 <= iq <= 125:
        res, comment = "🚀 Parlaq Beyin", "Səninlə söhbət etmək maraqlıdır, məntiqin güclüdür."
    elif 126 <= iq <= 145:
        res, comment = "⚡ Dahi", "Sən bu qrupda nə gəzirsən? Get NASA-da işə başla!"
    elif 146 <= iq <= 165:
        res, comment = "🌌 Kosmik Zəka", "Sənin beynin 2050-ci ildə yaşayır. Hər şeyi əvvəlcədən görürsən."
    elif 166 <= iq <= 199:
        res, comment = "🧬 Yeni Eynşteyn", "Sən sadəcə ağıllı deyilsən, sən yaşayan bir kompyutersən!"
    else: # 200 IQ
        res, comment = "👑 TANRI SƏVİYYƏSİ", "Sən bu kainatı yaradan kodları bilirsən sanki. Möhtəşəm!"

    final_zeka = (
        f"**╔════════════════════╗**\n"
        f"** 🧠 ZEKA ANALİZİ (V1)     **\n"
        f"**╚════════════════════╝**\n\n"
        f"👤 **İstifadəçi:** [{target.first_name}](tg://user?id={target.id})\n\n"
        f"📊 **Zəka Səviyyəsi (IQ):** `{iq}`\n"
        f"📌 **Status:** `{res}`\n\n"
        f"💬 **Botun Şərhi:** \n_{comment}_"
    )
    
    await status.edit_text(final_zeka)

  # --- 🍀 GÜNÜN ŞANSI ---
@app.on_message(filters.command("sans") & filters.group)
async def day_luck(client, message):
    status = await message.reply_text("🔮 **Kainatın enerjisi oxunur...**")
    await asyncio.sleep(0.8)
    
    love = random.randint(10, 100)
    money = random.randint(10, 100)
    health = random.randint(10, 100)
    
    luck_text = (
        f"**╔════════════════════╗**\n"
        f"** 🍀 GÜNÜN ŞANS ANALİZİ      **\n"
        f"**╚════════════════════╝**\n\n"
        f"👤 **İstifadəçi:** {message.from_user.first_name}\n\n"
        f"❤️ **Sevgi:** `% {love}`\n"
        f"💰 **Pul:** `% {money}`\n"
        f"🍏 **Sağlamlıq:** `% {health}`\n\n"
        f"✨ **Günün Məsləhəti:** "
    )
    
    advices = [
        "Bu gün risk etməkdən qorxma!", "Pulla ehtiyatlı ol, xərclərin arta bilər.",
        "Sevgidə yeni bir qığılcım gözlənilir.", "Sağlamlığına diqqət yetir, çox yorulma."
    ]
    
    await status.edit_text(luck_text + f"_{random.choice(advices)}_")
