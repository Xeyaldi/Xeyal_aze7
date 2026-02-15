import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    # Sənin təyin etdiyin sahibələr siyahısı
    OWNERS = [6241071228, 7592728364, 8024893255]
    ETIRAF_QRUPU = "sohbetqruprc"

    # --- 1. HELP (KÖMƏK MENYUSU) ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "📚 **ʙᴏᴛᴜɴ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı**\n\n"
            "📢 **ᴛᴀɢ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:**\n"
            "• `/tag`, `/utag`, `/flagtag`, `/tektag`, `/tagstop`\n\n"
            "🎮 **ᴏʏᴜɴʟᴀʀ:** `/basket`, `/futbol`, `/dart`, `/slot`, `/dice`\n\n"
            "🌍 **ᴍəʟᴜᴍᴀᴛ:**\n"
            "• `/hava [şəhər]`, `/valyuta`, `/wiki [mövzu]`, `/namaz [şəhər]`\n"
            "• `/tercume [dil]` - (Reply edərək)\n\n"
            "🤫 **ᴇᴛɪʀᴀғ:** `/etiraf` və ya `/acetiraf` [mesaj]\n\n"
            "🛡 **ᴀᴅᴍɪɴ:** `/purge` (Reply), `/id`, `/ping`"
        )
        await message.reply_text(help_text)

    # --- 2. ETİRAF SİSTEMİ (SAHİBƏ TƏSDİQLİ) ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: 
            return await message.reply_text("💬 Etirafınızı yazın. Məsələn: `/etiraf salam`")
        
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
            await message.reply_text("❌ Xəta: Sahibələr botu başlatmayıb.")

    # --- 3. TƏRCÜMƏ SİSTEMİ (YENİLƏNMİŞ - STABİL) ---
    @app.on_message(filters.command("tercume") & filters.reply)
    async def translate_func(client, message):
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text:
            return await message.reply_text("❌ Mətni olan bir mesajı reply edin.")

        # Dil xəritəsi (İstifadəçi dostu kodlar)
        lang_map = {
            "ing": "en", "en": "en", "ingilis": "en",
            "tr": "tr", "turk": "tr", "türk": "tr",
            "ru": "ru", "rus": "ru",
            "az": "az", "aze": "az",
            "de": "de", "alman": "de",
            "fr": "fr", "fransiz": "fr",
            "ar": "ar", "ereb": "ar"
        }

        cmd_lang = message.command[1].lower() if len(message.command) > 1 else "az"
        target_lang = lang_map.get(cmd_lang, cmd_lang)

        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10).json()
            translated_text = r[0][0][0]
            await message.reply_text(f"🌐 **Tərcümə ({target_lang.upper()}):**\n\n`{translated_text}`")
        except:
            await message.reply_text("❌ Tərcümə zamanı xəta. Dil kodunu yoxlayın (Məs: `/tercume en`).")

    # --- 4. HAVA DURUMU ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın.")
        city = message.command[1]
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid=b6907d289e10d714a6e88b30761fae22&units=metric&lang=az"
            r = requests.get(url, timeout=10).json()
            await message.reply_text(f"🌤 **{city.capitalize()}**\n🌡 Temperatur: {r['main']['temp']}°C\n☁️ Vəziyyət: {r['weather'][0]['description']}")
        except: await message.reply_text("❌ Şəhər tapılmadı.")

    # --- 5. VALYUTA ---
    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN", timeout=10).json()
            text = f"💰 **Məzənnə (AZN qarşı):**\n\n🇺🇸 USD: `{1/r['rates']['USD']:.2f}`\n🇪🇺 EUR: `{1/r['rates']['EUR']:.2f}`\n🇹🇷 TRY: `{1/r['rates']['TRY']:.2f}`\n🇷🇺 RUB: `{1/r['rates']['RUB']:.2f}`"
            await message.reply_text(text)
        except: await message.reply_text("❌ Məzənnə məlumatı alınmadı.")

    # --- 6. VİKİPEDİYA ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2: return
        query = message.text.split(None, 1)[1]
        try:
            res = requests.get(f"https://az.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}", timeout=10).json()
            await message.reply_text(f"📖 **{res['title']}**\n\n{res['extract']}\n\n[Daha ətraflı]({res['content_urls']['desktop']['page']})")
        except: await message.reply_text("❌ Məlumat tapılmadı.")

    # --- 7. NAMAZ VAXTLARI ---
    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        try:
            r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={urllib.parse.quote(city)}&country=Azerbaijan&method=3", timeout=10).json()
            t = r['data']['timings']
            await message.reply_text(f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n🌅 Sübh: `{t['Fajr']}`\n☀️ Zöhr: `{t['Dhuhr']}`\n🌆 Əsr: `{t['Asr']}`\n🌃 Axşam: `{t['Maghrib']}`\n🌌 İşaa: `{t['Isha']}`")
        except: await message.reply_text("❌ Xəta baş verdi.")

    # --- 8. PURGE (ADMİN) ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_func(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return await message.reply_text("Mesajı reply edin.")
        try:
            await client.delete_messages(message.chat.id, range(message.reply_to_message.id, message.id))
            await message.reply_text("🧹 Təmizləndi.")
        except: pass

    # --- 9. OYUNLAR ---
    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_func(client, message):
        emojis = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}
        await client.send_dice(message.chat.id, emoji=emojis[message.command[0]])
