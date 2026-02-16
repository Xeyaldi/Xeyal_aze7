import os, asyncio, requests, urllib.parse, random, wikipedia
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
    # Sənin verdiyin Owners məlumatları
    OWNERS = [6241071228, 7592728364, 8024893255]

    # --- KOMANDALARIN MENYUSU (Telegramda / yazanda siyahı çıxması üçün) ---
    async def set_commands():
        commands = [
            BotCommand("help", "📚 Botun geniş kömək menyusu"),
            BotCommand("valyuta", "💰 Günlük valyuta məzənnələri"),
            BotCommand("wiki", "📖 Vikipediyada geniş axtarış"),
            BotCommand("namaz", "🕋 Azərbaycan şəhərləri üçün namaz vaxtları"),
            BotCommand("tercume", "🌐 Mətni tərcümə edər (Reply)"),
            BotCommand("etiraf", "🤫 Tam gizli (anonim) etiraf"),
            BotCommand("acetiraf", "👤 Adınızla görünən etiraf"),
            BotCommand("purge", "🧹 Qrupda mesajları təmizləyər (Admin)"),
            BotCommand("id", "🆔 Sizin və qrupun ID-sini göstərər"),
            BotCommand("dice", "🎲 Şans zəri atar"),
            BotCommand("slot", "🎰 Slot maşını oyunu"),
            BotCommand("futbol", "⚽ Futbol oyunu"),
            BotCommand("basket", "🏀 Basketbol oyunu")
        ]
        await app.set_bot_commands(commands)

    # Botun ilk dəfə başlaması üçün /start komandası
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        await set_commands()
        await message.reply_text("✨ **Bot uğurla işə düşdü!**\n\nKomandalar siyahısı artıq `/` menyusunda aktivdir. `/help` yazaraq detallara baxa bilərsiniz.")

    # --- 1. HELP (NAXIŞLI DİZAYN) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "╔════════════════════╗\n"
            "   💠 **B O T  M E N Y U S U** 💠\n"
            "╚════════════════════╝\n\n"
            "📜 **Ümumi Komandalar:**\n"
            "🔹 `/help` - Bu menyunu göstərər.\n"
            "🔹 `/id` - ID məlumatlarını göstərər.\n"
            "🔹 `/ping` - Botun gecikməsini yoxlayar.\n\n"
            "🌍 **Məlumat və Faydalı:**\n"
            "🔹 `/valyuta` - Günlük Manat kursu.\n"
            "🔹 `/wiki [mövzu]` - Vikipediyadan ətraflı məlumat.\n"
            "🔹 `/namaz [şəhər]` - Gündəlik namaz vaxtları.\n"
            "🔹 `/tercume [dil]` - Reply ilə mətni tərcümə edər.\n\n"
            "🤫 **Etiraf Sistemi:**\n"
            "🔹 `/etiraf [mesaj]` - Sahibələrə anonim mesaj göndərər.\n"
            "🔹 `/acetiraf [mesaj]` - Adınızla birlikdə etiraf göndərər.\n\n"
            "🎮 **Əyləncə və Oyunlar:**\n"
            "🔹 `/dice`, `/basket`, `/futbol`, `/slot` - Şans oyunları.\n\n"
            "🛡 **Admin Alətləri:**\n"
            "🔹 `/purge` - Seçilən mesajdan aşağıdakıları silər.\n\n"
            "✨ *Bot heroku vasitəsilə 7/24 aktivdir!*"
        )
        await message.reply_text(help_text)

    # --- 2. ETİRAF SİSTEMİ ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: 
            return await message.reply_text("💬 **Etirafınızı yazın.**\nNümunə: `/etiraf Salam bot çox yaxşıdır.`")
        
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
            await message.reply_text("❌ Xəta: Sahibələr botu hələ başlatmayıb.")

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

    # --- 4. VALYUTA ---
    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN", timeout=10).json()
            rates = r.get('rates', {})
            usd = 1/rates['USD'] if 'USD' in rates else 0
            eur = 1/rates['EUR'] if 'EUR' in rates else 0
            try_rate = 1/rates['TRY'] if 'TRY' in rates else 0
            
            text = (f"💰 **Məzənnə (AZN qarşı):**\n\n"
                    f"🇺🇸 USD: `{usd:.2f}`\n"
                    f"🇪🇺 EUR: `{eur:.2f}`\n"
                    f"🇹🇷 TRY: `{try_rate:.2f}`")
            await message.reply_text(text)
        except: 
            await message.reply_text("❌ Məzənnə məlumatı alınmadı.")

    # --- 5. VİKİPEDİYA (GÜCLÜ SORĞU) ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2: return await message.reply_text("🔍 **Axtarılacaq mövzunu yazın.**")
        query = message.text.split(None, 1)[1]
        try:
            # Öncə kitabxana ilə sınayırıq
            wikipedia.set_lang("az")
            summary = wikipedia.summary(query, sentences=3)
            page = wikipedia.page(query)
            await message.reply_text(f"📖 **{page.title}**\n\n{summary}\n\n🔗 [Ətraflı oxu]({page.url})")
        except:
            # Kitabxana tapmasa API ilə sınayırıq
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                url = f"https://az.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code != 200: return await message.reply_text("❌ Məqalə tapılmadı.")
                res = r.json()
                await message.reply_text(f"📖 **{res['title']}**\n\n{res['extract'][:800]}...\n\n🔗 [Link]({res['content_urls']['desktop']['page']})")
            except:
                await message.reply_text("❌ Vikipediya ilə əlaqə kəsildi.")

    # --- 6. NAMAZ VAXTLARI ---
    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        try:
            r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={urllib.parse.quote(city)}&country=Azerbaijan&method=3", timeout=10).json()
            if r.get("code") != 200: return await message.reply_text("❌ Şəhər düzgün deyil.")
            t = r['data']['timings']
            await message.reply_text(f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n🌅 Sübh: `{t['Fajr']}`\n☀️ Zöhr: `{t['Dhuhr']}`\n🌆 Əsr: `{t['Asr']}`\n🌃 Axşam: `{t['Maghrib']}`\n🌌 İşaa: `{t['Isha']}`")
        except: 
            await message.reply_text("❌ Namaz vaxtları alınarkən xəta.")

    # --- 7. PURGE (ADMİN) ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return await message.reply_text("🧹 Silmək istədiyiniz yerin ilk mesajını reply edin.")
        try:
            message_ids = list(range(message.reply_to_message.id, message.id))
            for i in range(0, len(message_ids), 100):
                await client.delete_messages(message.chat.id, message_ids[i:i+100])
            
            await message.delete()
            done = await message.reply_text("🧹 Təmizləmə tamamlandı.")
            await asyncio.sleep(3)
            await done.delete()
        except: pass

    # --- 8. OYUNLAR ---
    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_func(client, message):
        emojis = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}
        try:
            cmd = message.command[0].lower()
            await client.send_dice(message.chat.id, emoji=emojis[cmd])
        except: pass

    # --- 9. ID GÖSTƏRMƏ ---
    @app.on_message(filters.command("id"))
    async def get_id(client, message):
        chat_id = message.chat.id
        user_id = message.from_user.id if message.from_user else "Bilinmir"
        await message.reply_text(f"🆔 **Sizin ID:** `{user_id}`\n🆔 **Çat ID:** `{chat_id}`")
