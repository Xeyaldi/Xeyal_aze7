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

    # --- 1. SAMBALLI HELP MENYUSU ---
    @app.on_message(filters.command("help"))
    async def help_cmd(client, message):
        help_text = (
            "✨ **ᴀʏsʙᴇʀǫ ᴛᴀɢ ʙᴏᴛ | ᴋᴏᴍᴀɴᴅᴀ ᴘᴀɴᴇʟɪ** ✨\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "🌍 **ᴍəʟᴜᴍᴀᴛ ᴠə ᴀʟəᴛʟəʀ:**\n"
            "• `/hava [şəhər]` — Anlıq hava durumu\n"
            "• `/wiki [mövzu]` — Vikipediyadan məlumat\n"
            "• `/valyuta` — Güncəl məzənnələr\n"
            "• `/namaz [şəhər]` — Namaz vaxtları\n\n"
            "🔄 **ᴛəʀᴄüᴍə sɪsᴛᴇᴍɪ:**\n"
            "• `/tercume [dil]` — Mesajı reply edərək yazın.\n"
            "👉 **ᴅɪʟʟəʀ:** `ing` (İngilis), `tr` (Türk), `rus` (Rus), `az` (Azərbaycan)\n\n"
            "🎭 **əʏʟəɴᴄə ᴠə sᴏsɪᴀʟ:**\n"
            "• `/love [@istifadeci]` — Sevgi testi yoxla\n"
            "• `/kimem` — Profil analizi (Zarafat)\n"
            "• `/qerar [sual]` — Bot sizin üçün qərar verir\n"
            "• `/gununsozu` — Motivasiya edici sözlər\n\n"
            "🤫 **ᴇᴛɪʀᴀғ sɪsᴛᴇᴍɪ:**\n"
            "• `/etiraf [mesaj]` — Anonim etiraf (Admin təsdiqli)\n"
            "• `/acetiraf [mesaj]` — Adınızla etiraf\n\n"
            "🎮 **ᴏʏᴜɴʟᴀʀ:** `/basket`, `/futbol`, `/dart`, `/slot`, `/dice`\n"
            "🛡 **ᴀᴅᴍɪɴ:** `/purge` (Reply), `/id`, `/ping`\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await message.reply_text(help_text)

    # --- 2. VİKİPEDİYA (STABİL) ---
    @app.on_message(filters.command("wiki"))
    async def wiki_search(client, message):
        if len(message.command) < 2: return
        query = " ".join(message.command[1:]).strip()
        safe_query = urllib.parse.quote(query.replace(" ", "_"))
        try:
            url = f"https://az.wikipedia.org/api/rest_v1/page/summary/{safe_query}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
            if "extract" in r:
                msg = f"📖 **{r.get('title')}**\n\n{r.get('extract')}\n\n🔗 [Daha çox oxu]({r.get('content_urls', {}).get('desktop', {}).get('page')})"
                await message.reply_text(msg, disable_web_page_preview=False)
            else: await message.reply_text(f"❌ '{query}' tapılmadı.")
        except: await message.reply_text("❌ Wiki serveri cavab vermir.")

    # --- 3. HAVA DURUMU (STABİL) ---
    @app.on_message(filters.command("hava"))
    async def get_weather(client, message):
        if len(message.command) < 2: return
        u_input = " ".join(message.command[1:]).strip().lower()
        repls = {'ə': 'e', 'ı': 'i', 'ç': 'c', 'ş': 's', 'ğ': 'g', 'ö': 'o', 'ü': 'u'}
        city_clean = "".join(repls.get(c, c) for c in u_input)
        if city_clean == "baki": city_clean = "Baku"
        try:
            url = f"https://wttr.in/{urllib.parse.quote(city_clean)}?format=%l:+%c+%t+%C"
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if res.status_code == 200 and "Unknown" not in res.text:
                await message.reply_text(f"🌤 **Hava:** `{res.text.strip()}`")
            else: await message.reply_text("❌ Şəhər tapılmadı.")
        except: await message.reply_text("❌ Hava xətası.")

    # --- 4. TƏRCÜMƏ ---
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
        except: await message.reply_text("❌ Xəta.")

    # --- 5. SEVGİ TESTİ (💘) ---
    @app.on_message(filters.command("love"))
    async def love_test(client, message):
        if len(message.command) < 2: return await message.reply_text("❤️ Kimlərin uyğunluğunu yoxlamaq istəyirsən?")
        u1 = message.from_user.first_name
        u2 = message.text.split(None, 1)[1]
        p = random.randint(0, 100)
        s = "💔 Ayrılın, xeyir yoxdur..." if p < 30 else "💛 Dost qalsanız yaxşıdır." if p < 70 else "💖 Toy nə vaxtdır?"
        await message.reply_text(f"💘 **Sevgi Testi**\n\n👤 {u1} + {u2}\n📊 Uyğunluq: **{p}%**\n📝 Qərar: {s}")

    # --- 6. KİMƏM (😎) ---
    @app.on_message(filters.command("kimem"))
    async def who_am_i(client, message):
        roles = ["Qrupun ağsaqqalı 🧔", "Daimi yatmış 😴", "Müzakirə ustası 🗣", "Hər şeyə etiraz edən 🙅‍♂️", "Qrupun gizli qəhrəmanı 🦸‍♂️", "Hər mesajda tag edən 📢"]
        await message.reply_text(f"🔍 **Profil Analizi:**\n\nSən: **{random.choice(roles)}**")

    # --- 7. QƏRAR VERİCİ (🔮) ---
    @app.on_message(filters.command("qerar"))
    async def decide_func(client, message):
        if len(message.command) < 2: return
        opts = ["Bəli, mütləq!", "Xeyr, məsləhət deyil.", "Bir az gözlə, sonra baxarıq.", "Məncə hə, amma yenə də sən bilərsən."]
        await message.reply_text(f"🔮 **Botun Qərarı:**\n\n`{random.choice(opts)}`")

    # --- 8. GÜNÜN SÖZÜ (📜) ---
    @app.on_message(filters.command("gununsozu"))
    async def daily_quote(client, message):
        quotes = ["Həyat planlar qurarkən başına gələnlərdir.", "Ən böyük risk, riskə girməməkdir.", "Sükut ən güclü qışqırıqdır.", "Bu gün gözəl bir şey olacaq!"]
        await message.reply_text(f"📜 **Günün Sözü:**\n\n`{random.choice(quotes)}`")

    # --- 9. ETİRAF SİSTEMİ ---
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

    # --- 10. VALYUTA & NAMAZ ---
    @app.on_message(filters.command("valyuta"))
    async def get_valyuta(client, message):
        try:
            r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
            await message.reply_text(f"💰 **Məzənnə:**\n🇺🇸 USD: `{1/r['rates']['USD']:.2f}`\n🇪🇺 EUR: `{1/r['rates']['EUR']:.2f}`\n🇹🇷 TRY: `{1/r['rates']['TRY']:.2f}`")
        except: await message.reply_text("❌ Xəta.")

    @app.on_message(filters.command("namaz"))
    async def namaz_times(client, message):
        city = message.command[1] if len(message.command) > 1 else "Baku"
        try:
            r = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3").json()
            t = r['data']['timings']
            await message.reply_text(f"🕋 **{city.capitalize()} Namazı**\n\n🌅 Sübh: `{t['Fajr']}` | ☀️ Zöhr: `{t['Dhuhr']}`\n🌆 Əsr: `{t['Asr']}` | 🌃 Axşam: `{t['Maghrib']}`")
        except: await message.reply_text("❌ Namaz vaxtı tapılmadı.")

    # --- 11. ADMİN & OYUNLAR ---
    @app.on_message(filters.command("purge") & filters.group)
    async def purge_f(client, message):
        if not await check_admin(client, message, OWNERS): return
        if not message.reply_to_message: return
        await client.delete_messages(message.chat.id, range(message.reply_to_message.id, message.id))

    @app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
    async def games_f(client, message):
        e = {"basket":"🏀", "futbol":"⚽", "dart":"🎯", "slot":"🎰", "dice":"🎲"}
        await client.send_dice(message.chat.id, emoji=e[message.command[0]])
