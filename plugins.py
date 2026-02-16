import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.enums import ChatMemberStatus, ChatType

# --- YARDIMÇI FUNKSİYA: ADMİN YOXLAMA ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

def init_plugins(app, get_db_connection):
    OWNERS = [6241071228, 7592728364, 8024893255]
    WEATHER_API_KEY = "07f6c94ce1ce87c4ad51a713b186762f"

    # --- KOMANDALARIN MENYUSUNU QEYDƏ ALMAQ (Telegramda / yazanda çıxması üçün) ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Kömək menyusunu göstərər"),
            BotCommand("hava", "🌤 Hava durumu (məs: /hava Bakı)"),
            BotCommand("valyuta", "💰 Günlük məzənnələr"),
            BotCommand("wiki", "📖 Vikipediyada axtarış"),
            BotCommand("namaz", "🕋 Namaz vaxtları"),
            BotCommand("tercume", "🌐 Mətni tərcümə edər (Reply)"),
            BotCommand("etiraf", "🤫 Anonim etiraf göndərər"),
            BotCommand("acetiraf", "👤 Adlı etiraf göndərər"),
            BotCommand("purge", "🧹 Mesajları təmizləyər (Admin)"),
            BotCommand("dice", "🎲 Zər atar"),
            BotCommand("slot", "🎰 Şans oyunu"),
            BotCommand("futbol", "⚽ Futbol oyunu")
        ]
        await app.set_bot_commands(commands)

    # Bot işə düşəndə komandaları yüklə
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await set_commands()
        await message.reply_text("✨ **Bot aktivdir!**\nKomandaları görmək üçün `/` yazın və ya `/help` göndərin.")

    # --- 1. HELP (KÖMƏK MENYUSU - TƏKMİLLƏŞMİŞ) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **B O T  M E N Y U S U** 💠\n"
            "╚════════════════════╝\n\n"
            "📜 **Ümumi Komandalar:**\n"
            "🔹 `/help` - Bu menyunu göstərər.\n"
            "🔹 `/id` - Sizin və ya qrupun ID-sini göstərər.\n"
            "🔹 `/ping` - Botun sürətini yoxlayar.\n\n"
            "🌍 **Məlumat & Faydalı:**\n"
            "🔹 `/hava [şəhər]` - Yazdığınız şəhərin hava durumunu göstərər.\n"
            "🔹 `/valyuta` - Manatın digər valyutalara nisbətini göstərər.\n"
            "🔹 `/wiki [mövzu]` - Vikipediyadan məlumat gətirər.\n"
            "🔹 `/namaz [şəhər]` - Gündəlik namaz vaxtlarını göstərər.\n"
            "🔹 `/tercume [dil]` - Reply etdiyiniz mətni istədiyiniz dilə çevirər.\n\n"
            "🤫 **Etiraf Sistemi:**\n"
            "🔹 `/etiraf [mesaj]` - Tam anonim (gizli) mesaj göndərər.\n"
            "🔹 `/acetiraf [mesaj]` - Adınızla birlikdə etiraf göndərər.\n\n"
            "🎮 **Əyləncə & Oyunlar:**\n"
            "🔹 `/dice`, `/basket`, `/futbol`, `/dart`, `/slot` - Şansınızı yoxlayın!\n\n"
            "🛡 **Admin Paneli:**\n"
            "🔹 `/purge` - Reply etdiyiniz mesajdan sonrakıları silər.\n"
            "🔹 `/tagstop` - Davam edən tağı dayandırar.\n\n"
            "✨ *Daha çoxu üçün botu izləməyə davam edin!*"
        )
        await message.reply_text(help_text)

    # --- 2. ETİRAF SİSTEMİ ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: 
            return await message.reply_text("💬 **Etirafınızı yazın.**\nMəsələn: `/etiraf botu çox sevdim`.")
        
        txt = message.text.split(None, 1)[1]
        is_anon = message.command[0] == "etiraf"
        sender_info = "Anonim" if is_anon else f"{message.from_user.first_name} ({message.from_user.id})"
        
        check_buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"accept_etiraf|{message.from_user.id}"),
                InlineKeyboardButton("❌ Rədd et", callback_data="reject_etiraf")
            ]
        ])
        
        count = 0
        for owner_id in OWNERS:
            try:
                await client.send_message(
                    owner_id, 
                    f"📩 **Yeni Etiraf Təsdiq Gözləyir!**\n\n👤 **Kimdən:** {sender_info}\n💬 **Mesaj:** `{txt}`",
                    reply_markup=check_buttons
                )
                count += 1
            except: continue
        
        if count > 0:
            await message.reply_text("✅ Etirafınız təsdiq üçün sahibələrə göndərildi.")
        else:
            await message.reply_text("❌ Xəta: Bot sahiblərinə ulaşıla bilmədi.")

    # --- 3. TƏRCÜMƏ SİSTEMİ ---
    @app.on_message(filters.command("tercume") & filters.reply)
    async def translate_func(client, message):
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text:
            return await message.reply_text("❌ Mətni olan bir mesajı reply edin.")

        lang_map = {"ing": "en", "en": "en", "turk": "tr", "türk": "tr", "ru": "ru", "aze": "az", "az": "az"}
        cmd_lang = message.command[1].lower() if len(message.command) > 1 else "az"
        target_lang = lang_map.get(cmd_lang, cmd_lang)

        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
            translated_text = "".join([s[0] for s in r[0] if s[0]])
            await message.reply_text(f"🌐 **Tərcümə ({target_lang.upper()}):**\n\n`{translated_text}`")
        except:
            await message.reply_text("❌ Tərcümə zamanı xəta baş verdi.")

    # --- 4. HAVA DURUMU (YENİ API İLƏ) ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın.\nMəsələn: `/hava Bakı`")
        city = message.text.split(None, 1)[1]
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid={WEATHER_API_KEY}&units=metric&lang=az"
            r = requests.get(url, timeout=10).json()
            if r.get("cod") != 200: return await message.reply_text("❌ Şəhər tapılmadı.")
            
            temp = r['main']['temp']
            desc = r['weather'][0]['description']
            await message.reply_text(f"🌤 **Hava Durumu: {city.capitalize()}**\n🌡 Temperatur: {temp}°C\n☁️ Vəziyyət: {desc.capitalize()}")
        except: await message.reply_text("❌ Hava məlumatı alınmadı.")

    # --- 5. VALYUTA ---
    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN", timeout=10).json()
            usd = 1/r['rates']['USD']
            eur = 1/r['rates']['EUR']
            try_rate = 1/r['rates']['TRY']
            rub = 1/r['rates']['RUB']
            text = (f"💰 **Məzənnə (AZN qarşı):**\n\n"
                    f"🇺🇸 USD: `{usd:.2f}`\n"
                    f"🇪🇺 EUR: `{eur:.2f}`\n"
                    f"🇹🇷 TRY: `{try_rate:.2f}`\n"
                    f"🇷🇺 RUB: `{rub:.2f}`")
            await message.reply_text(text)
        except: await message.reply_text("❌ Məzənnə məlumatı alınmadı.")

    # --- 6. VİKİPEDİYA (GÜCLƏNDİRİLMİŞ) ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2: return await message.reply_text("🔍 Nəyi axtarmaq istəyirsiniz?")
        query = message.text.split(None, 1)[1]
        try:
            res = requests.get(f"https://az.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}", timeout=10).json()
            if "extract" not in res: return await message.reply_text("❌ Məlumat tapılmadı.")
            await message.reply_text(f"📖 **{res['title']}**\n\n{res['extract']}\n\n🔗 [Daha ətraflı]({res['content_urls']['desktop']['page']})")
        except: await message.reply_text("❌ Vikipediya xətası.")

    # --- 7. NAMAZ VAXTLARI ---
    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        try:
            r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={urllib.parse.quote(city)}&country=Azerbaijan&method=3", timeout=10).json()
            t = r['data']['timings']
            await message.reply_text(f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n🌅 Sübh: `{t['Fajr']}`\n☀️ Zöhr: `{t['Dhuhr']}`\n🌆 Əsr: `{t['Asr']}`\n🌃 Axşam: `{t['Maghrib']}`\n🌌 İşaa: `{t['Isha']}`")
        except: await message.reply_text("❌ Vaxtlar alınarkən xəta oldu.")

    # --- 8. PURGE (ADMİN) ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return await message.reply_text("🧹 Silmək istədiyiniz yerin ilk mesajını reply edin.")
        try:
            message_ids = list(range(message.reply_to_message.id, message.id))
            for i in range(0, len(message_ids), 100):
                await client.delete_messages(message.chat.id, message_ids[i:i+100])
            done = await message.reply_text("🧹 Təmizləmə tamamlandı.")
            await asyncio.sleep(3)
            await done.delete()
        except: pass

    # --- 9. OYUNLAR ---
    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_func(client, message):
        emojis = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}
        try:
            await client.send_dice(message.chat.id, emoji=emojis[message.command[0].lower()])
        except: pass
