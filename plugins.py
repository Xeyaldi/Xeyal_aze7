import os, asyncio, requests, urllib.parse, time
from pyrogram import filters
from pyrogram.types import BotCommand

def init_plugins(app, get_db_connection):
    # --- 14. 🕵️ KİM SİLDİ? (LOG SİSTEMİ) ---
    @app.on_deleted_messages()
    async def deleted_log(c, m):
        for msg in m:
            if msg.text:
                print(f"🗑 Silinən Mesaj: {msg.text} (ID: {msg.from_user.id if msg.from_user else 'Bilinmir'})")

    # --- 15. 📊 Qrup Analitika (Mesaj Sayı) ---
    @app.on_message(filters.group & ~filters.bot, group=4)
    async def count_messages(c, m):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO user_stats (user_id, msg_count) VALUES (%s, 1) ON CONFLICT (user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (m.from_user.id,))
        conn.commit(); cur.close(); conn.close()

    @app.on_message(filters.command("top"))
    async def top_users(c, m):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT user_id, msg_count FROM user_stats ORDER BY msg_count DESC LIMIT 5")
        res = cur.fetchall(); cur.close(); conn.close()
        text = "🏆 **Qrupun Ən Aktivləri:**\n\n"
        for i, r in enumerate(res, 1): text += f"{i}. ID: `{r[0]}` — {r[1]} mesaj\n"
        await m.reply_text(text)

    # --- 16. 🕒 Xatırladıcı (REMINDER) ---
    @app.on_message(filters.command("xatirlat"))
    async def remind_me(c, m):
        if len(m.command) < 3: return await m.reply_text("ℹ️ `/xatirlat 10m Çörək al` formatında yazın.")
        sure = m.command[1]
        text = m.text.split(None, 2)[2]
        await m.reply_text(f"✅ **Oldu!** {sure} sonra sizə bildirəcəm.")
        seconds = int(sure[:-1]) * 60 if 'm' in sure else int(sure[:-1]) * 3600
        await asyncio.sleep(seconds)
        await m.reply_text(f"🔔 **XATIRLATMA!**\n\n📌: {text}", reply_to_message_id=m.id)

    # --- 17. 🎲 Qumar (🎰 SLOT) ---
    @app.on_message(filters.command("slot"))
    async def slot_machine(c, m):
        res = await c.send_dice(m.chat.id, emoji="🎰")
        if res.dice.value in [1, 22, 43, 64]: await m.reply_text("🎊 **TEBRİKLER! Qazandınız!**")

    # --- 18. 📝 Word/Text to PDF ---
    @app.on_message(filters.command("pdf"))
    async def make_pdf(c, m):
        if len(m.command) < 2: return
        from reportlab.pdfgen import canvas
        text = m.text.split(None, 1)[1]
        pdf_file = f"doc_{m.from_user.id}.pdf"
        can = canvas.Canvas(pdf_file)
        can.drawString(100, 750, text)
        can.save()
        await m.reply_document(pdf_file, caption="📄 Mətniniz PDF-ə çevrildi.")
        os.remove(pdf_file)

    # --- 19. 🕵️ Profil Kimliyi (WHOIS) ---
    @app.on_message(filters.command("whois"))
    async def who_is(c, m):
        user = m.reply_to_message.from_user if m.reply_to_message else m.from_user
        text = (f"👤 **İstifadəçi Məlumatı:**\n\n"
                f"🏷 Ad: {user.first_name}\n"
                f"🆔 ID: `{user.id}`\n"
                f"🔗 Link: [Profile](tg://user?id={user.id})\n"
                f"🤖 Bot: {'Bəli' if user.is_bot else 'Xeyr'}")
        await m.reply_text(text)

    # --- 20. 🧪 Şifrə Yoxlayıcı ---
    @app.on_message(filters.command("yoxla"))
    async def check_pass(c, m):
        if len(m.command) < 2: return
        p = m.command[1]
        status = "Zəif 🔴" if len(p) < 6 else "Güclü 🟢"
        await m.reply_text(f"🔑 Şifrə dərəcəsi: **{status}**")

    # --- 21. 🎬 Film Axtarışı (IMDB) ---
    @app.on_message(filters.command("film"))
    async def film_search(c, m):
        if len(m.command) < 2: return
        query = urllib.parse.quote(m.text.split(None, 1)[1])
        r = requests.get(f"http://www.omdbapi.com/?t={query}&apikey=784a9e9e").json()
        if r.get("Response") == "True":
            await m.reply_text(f"🎬 **{r['Title']}** ({r['Year']})\n⭐️ Reytinq: {r['imdbRating']}\n🎭 Janr: {r['Genre']}\n📖 Mövzu: {r['Plot']}")
        else: await m.reply_text("❌ Film tapılmadı.")

    # --- 22. 💎 Bonus: Zəng (Prank Call Məqsədli) ---
    @app.on_message(filters.command("zeng"))
    async def prank_call(c, m):
        await m.reply_text("📞 İstifadəçi ilə zəng bağlantısı qurulur... 📵 Xəta: Qarşı tərəf məşğuldur.")

    # --- 23. 🌍 IP Info ---
    @app.on_message(filters.command("ip"))
    async def ip_info(c, m):
        if len(m.command) < 2: return
        ip = m.command[1]
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        await m.reply_text(f"🌐 **IP:** {ip}\n📍 Ölkə: {r.get('country')}\n🏙 Şəhər: {r.get('city')}\n📡 ISP: {r.get('isp')}")

    # --- 24. 🌙 Gecə Modu (Admin) ---
    @app.on_message(filters.command("gece") & filters.group)
    async def night_mode(c, m):
        # is_admin funksiyası bot.py daxilindədir, ona görə birbaşa işləyəcək
        await m.reply_text("🌙 **Gecə modu aktiv edildi.** Artıq qrupda yalnız adminlər yaza bilər (Simulyasiya).")

    # --- 25. ⚡️ Ping Sürəti ---
    @app.on_message(filters.command("ping"))
    async def ping_speed(c, m):
        start = time.time()
        msg = await m.reply_text("🚀")
        end = time.time()
        await msg.edit_text(f"⚡️ **Bot Sürəti:** `{(end - start) * 1000:.2f} ms`")
