import os, asyncio, requests, urllib.parse, random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType

# --- ADMİN YOXLAMA FUNKSİYASI ---
async def check_admin(client, message, owners):
    if message.chat.type == ChatType.PRIVATE: return True
    if message.from_user and message.from_user.id in owners: return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except: return False

def init_plugins(app, get_db_connection):
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

    # --- 2. VİKİPEDİYA (KÖKLÜ DÜZƏLİŞ ✅) ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2:
            return await message.reply_text("📖 Axtarmaq istədiyiniz mövzunu yazın. Məs: `/wiki Baki`")
        
        query = " ".join(message.command[1:]).strip()
        # API üçün mətni formatlayırıq (Boşluqları '_' edirik və xüsusi hərfləri kodlayırıq)
        safe_query = urllib.parse.quote(query.replace(" ", "_"))
        
        try:
            # Wikimedia API - daha stabil və dəqiq axtarış
            url = f"https://az.wikipedia.org/api/rest_v1/page/summary/{safe_query}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
            
            if "extract" in r:
                title = r.get("title", query)
                extract = r.get("extract", "Məlumat tapılmadı.")
                link = r.get("content_urls", {}).get("desktop", {}).get("page", "")
                
                msg = f"📖 **{title}**\n\n{extract}\n\n🔗 [Daha çox oxu]({link})"
                await message.reply_text(msg, disable_web_page_preview=False)
            else:
                await message.reply_text(f"❌ '{query}' haqqında məlumat tapılmadı. Mövzunu tam yazın.")
        except:
            await message.reply_text("❌ Vikipediya ilə əlaqə kəsildi.")

    # --- 3. HAVA DURUMU (STABİL wttr.in METODU ✅) ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın.")
        city = message.command[1].lower()
        repls = {'ə': 'e', 'ı': 'i', 'ç': 'c', 'ş': 's', 'ğ': 'g', 'ö': 'o', 'ü': 'u'}
        city_clean = "".join(repls.get(c, c) for c in city)
        try:
            # wttr.in API key istəmir və Azərbaycan hərfləri ilə problem yaratmır
            url = f"https://wttr.in/{city_clean}?format=%l:+%c+%t+%C"
            res = requests.get(url, timeout=10)
            if res.status_code == 200 and "Unknown" not in res.text:
                await message.reply_text(f"🌤 **Hava Durumu:**\n`{res.text.strip()}`")
            else:
                await message.reply_text("❌ Şəhər tapılmadı. Məsələn: `/hava baki` yazın.")
        except:
            await message.reply_text("❌ Hava serverində xəta.")

    # --- 4. ETİRAF SİSTEMİ (SAHİBƏ TƏSDİQLİ) ---
    @app.on_message(filters.command(["etiraf", "acetiraf"]))
    async def etiraflar(client, message):
        if len(message.command) < 2: return
        txt = message.text.split(None, 1)[1]
        is_a = message.command[0] == "etiraf"
        sender = "Anonim" if is_a else f"{message.from_user.first_name}"
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"accept_etiraf|{message.from_user.id}"), InlineKeyboardButton("❌ Rədd et", callback_data="reject_etiraf")]])
        for oid in OWNERS:
            try: await client.send_message(oid, f"📩 **Etiraf:**\n👤 Kimdən: {sender}\n💬 Mesaj: `{txt}`", reply_markup=btn)
            except: continue
        await message.reply_text("✅ Təsdiq üçün sahibələrə göndərildi.")

    # --- 5. TƏRCÜMƏ SİSTEMİ ---
    @app.on_message(filters.command("tercume") & filters.reply)
    async def translate_func(client, message):
        text = message.reply_to_message.text or message.reply_to_message.caption
        if not text: return
        l_map = {"ing": "en", "tr": "tr", "rus": "ru", "az": "az", "en": "en"}
        cmd_l = message.command[1].lower() if len(message.command) > 1 else "az"
        t_l = l_map.get(cmd_l, cmd_l)
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={t_l}&dt=t&q={urllib.parse.quote(text)}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
            await message.reply_text(f"🌐 **Tərcümə ({t_l.upper()}):**\n`{r[0][0][0]}`")
        except: await message.reply_text("❌ Tərcümə xətası.")

    # --- 6. NAMAZ VAXTLARI ---
    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        try:
            r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3").json()
            t = r['data']['timings']
            await message.reply_text(f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n🌅 Sübh: `{t['Fajr']}`\n☀️ Zöhr: `{t['Dhuhr']}`\n🌆 Əsr: `{t['Asr']}`\n🌃 Axşam: `{t['Maghrib']}`")
        except: await message.reply_text("❌ Namaz vaxtı tapılmadı.")

    # --- 7. VALYUTA ---
    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
            await message.reply_text(f"💰 **Məzənnə:**\n🇺🇸 USD: `{1/r['rates']['USD']:.2f}`\n🇪🇺 EUR: `{1/r['rates']['EUR']:.2f}`\n🇹🇷 TRY: `{1/r['rates']['TRY']:.2f}`")
        except: await message.reply_text("❌ Xəta.")

    # --- 8. PURGE & OYUNLAR ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_f(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        await client.delete_messages(message.chat.id, range(message.reply_to_message.id, message.id))

    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_f(client, message):
        e = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}
        await client.send_dice(message.chat.id, emoji=e[message.command[0]])
