import os, asyncio, random, psycopg2, requests, urllib.parse, time, importlib
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import asyncio
import openai
from pyrogram import enums
import asyncio
import random
import requests
import urllib.parse
import google.generativeai as genai  # Bu AI kitabxanasıdır
from pyrogram import Client, filters
from pyrogram.enums import ChatType

import google.generativeai as genai

# Nunu AI Ayarları
GEMINI_KEY = "AIzaSyDDCm8i8cPtKOjHPK57um6yL45n6Zf5ta8" 
genai.configure(api_key=GEMINI_KEY)

NUNU_PROMPT = """
Sənin adın Nunudur. Sən çox mehriban, şirin və köməkçil bir Azərbaycanlı qızsan. 
İstifadəçilərlə danışarkən "canım", "balam", "şirinim", "əzizim" kimi səmimi sözlər işlədirsən. 
Sən robot deyilsən, sanki bir insanın yaxın dostusan. 
Azərbaycan dilində çox təbii danışırsan və həmişə pozitivsən.
"""

nunu_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=NUNU_PROMPT
)

chat_sessions = {}
# --- PLUGİNS FAYLINI TANIMAQ ÜÇÜN KÖRPÜ (YENİ) ---
def load_plugins(client):
    # plugin.py faylı varsa onu yükləyir
    if os.path.exists("plugin.py"):
        try:
            importlib.import_module("plugin")
            print("✅ plugin.py tanındı!")
        except Exception as e:
            print(f"❌ plugin.py xətası: {e}")
    
    # plugins qovluğu varsa içindəki hər şeyi yükləyir
    if os.path.exists("plugins"):
        for file in os.listdir("plugins"):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = f"plugins.{file[:-3]}"
                try:
                    importlib.import_module(module_name)
                except:
                    pass
                    
# --- AYARLAR ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

OWNERS = [8568941859, 8371395083, 8024893255] 
SAHIBE_ID = 8024893255
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 
SOHBET_QRUPU = "https://t.me/ht_bots" 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tag_process = {}
chatbot_status = {}
link_block_status = {}

# ----------------- SİYAHLAR (HEÇ NƏ SİLİNMƏYİB) -----------------
BAYRAQLAR = ["🇦🇿","🇹🇷","🇵🇰","🇺🇿","🇰🇿","🇰🇬","🇹🇲","🇦🇱","🇩🇿","🇦🇸","🇦🇩","🇦🇴","🇦🇮","🇦🇶","🇦🇬","🇦🇷","🇦🇲","🇦🇼","🇦🇺","🇦🇹","🇧🇸","🇧🇭","🇧🇩","🇧🇧","🇧🇪","🇧🇿","🇧🇯","🇧🇲","🇧🇹","🇧🇴","🇧🇦","🇧🇼","🇧🇷","🇮🇴","🇻🇬","🇧🇳","🇧🇬","🇧🇫","🇧🇮","🇰🇭","🇨🇲","🇨🇦","🇮🇨","🇨🇻","🇧","🇰🇾","🇨🇫","🇹🇩","🇨🇱","🇨🇳","🇨🇽","🇨🇨","🇨🇴","🇰🇲","🇨🇬","🇨🇩","🇨🇰","🇨🇷","🇨🇮","🇭🇷","🇨🇺","🇨🇼","🇨🇾","🇨🇿","🇩🇰","🇩🇯","🇩🇲","🇩🇴","🇪🇨","🇪🇬","🇸🇻","🇬","🇪🇷","🇪🇪","🇪🇹","🇪🇺","🇫🇰","🇫🇴","🇫🇯","🇫🇮","🇫🇷","🇬🇫","🇵🇫","🇹🇫","🇬🇦","🇬🇲","🇬🇪","🇩🇪","🇬🇭","🇬🇮","🇬🇷","🇬🇱","🇬🇩","🇬🇵","🇬🇺","🇬🇹","🇬🇬","🇬🇳","🇬🇼","🇬🇾","🇭🇹","🇭🇳","🇭🇰","🇭🇺","🇮🇸","🇮🇳","🇮🇩","🇮🇷","🇮","🇮🇪","🇮🇲","🇮🇱","🇮🇹","🇯🇲","🇯🇵","🇯🇪","🇯🇴","🇰🇪","🇰🇮","🇽🇰","🇰🇼","🇱🇦","🇱🇻","🇱🇧","🇱🇸","🇱🇷","🇱🇾","🇱🇮","🇱🇹","🇱🇺","🇲🇴","🇲🇰","🇲🇬","🇲🇼","🇲🇾","🇲🇻","🇲🇱","🇲🇹","🇲🇭","🇲","🇲🇷","🇲🇺","🇾🇹","🇲🇽","🇫🇲","🇲🇩","🇲🇨","🇲🇳","🇲🇪","🇲🇸","🇲🇦","🇲🇿","🇲🇲","🇳🇦","🇳🇷","🇳🇵","🇳🇱","🇳🇨","🇳🇿","🇳🇮","🇳🇪","🇳🇬","🇳🇺","🇳🇫","🇰🇵","🇲🇵","🇳🇴","🇴🇲","🇵🇦","🇵🇬","🇵🇾","🇵🇪","🇵🇭","🇵🇳","🇵🇱","🇵🇹","🇵🇷","🇶🇦","🇷🇪","🇷🇴","🇷🇺","🇷🇼","🇼🇸","🇸🇲","🇸🇹","🇸🇦","🇸🇳","🇷🇸","🇸🇨","🇸🇱","🇸🇬","🇸🇽","🇸🇰","🇸🇮","🇬🇸","🇸🇧","🇸🇴","🇿🇦","🇰🇷","🇸🇸","🇪🇸","🇱🇰","🇧🇱","🇸🇭","🇰🇳","🇱🇨","🇵🇲","🇻🇨","🇸🇩","🇸🇷","🇸🇿","🇸🇪","🇨🇭","🇸🇾","🇹🇼","🇹🇯","🇹🇿","🇹🇭","🇹🇱","🇹🇬","🇹🇰","🇹🇴","🇹🇹","🇹🇳","🇹🇲","🇹🇨","🇹🇻","🇺🇬","🇺🇦","🇦🇪","🇬🇧","🇺🇸","🇺🇾","🇻🇮","🇻🇺","🇻🇦","🇻🇪","🇻🇳","🇼🇫","🇪🇭","🇾🇪","🇿🇲","🇿🇼"]
EMOJILER = ["🌈","🪐","🎡","🍭","💎","🔮","⚡","🔥","🚀","🛸","🎈","🎨","🎭","🎸","👾","🧪","🧿","🍀","🍿","🎁","🔋","🧸","🎉","✨","🌟","🌙","☀️","☁️","🌊","🌋","☄️","🍄","🌹","🌸","🌵","🌴","🍁","🍎","🍓","🍍","🥥","🍔","🍕","🍦","🍩","🥤","🍺","🚲","🏎️","🚁","⛵","🛰️","📱","💻","💾","📸","🎥","🏮","🎬","🎧","🎤","🎹","🎺","🎻","🎲","🎯","🎮","🧩","🦄","🦁","🦊","🐼","🐨","🐯","🐝","🦋","🦜","🐬","🐳","🐾","🐉"]
CB_SOZLER = ["Salam","Necəsən?","Nə var nə yox?","Hardasan?","Xoş gəldin","Sağ ol","Buyur","Bəli","Xeyr","Əlbəttə","Can","Nolsun?","Gözəl","Bomba kimi","İşdəyəm","Evdəyəm","Yoldayam","Nə edirsən?","Heç nə","Sən nə edirsən?","Məzələnirsən?","Vay vay","Ay can","Oldu"]

# --- DATABASE ---
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS broadcast_list (chat_id BIGINT PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS brain (content TEXT, chat_id BIGINT)")
    cur.execute("CREATE TABLE IF NOT EXISTS qadaga_list (word TEXT PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS user_history (user_id BIGINT, old_name TEXT, old_username TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS user_stats (user_id BIGINT PRIMARY KEY, msg_count INT DEFAULT 0)")
    conn.commit()
    cur.close()
    conn.close()

init_db()

# --- ADMIN YOXLAMASI ---
async def is_admin(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return True
    if message.from_user and message.from_user.id in OWNERS:
        return True
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except:
        return False

# --- START MESAJI ---
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO broadcast_list (chat_id) VALUES (%s) ON CONFLICT DO NOTHING", (message.chat.id,))
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass

    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👨‍💻 sᴀʜɪʙ", url="https://t.me/Kullaniciadidi"), InlineKeyboardButton("🐦‍🔥 ʙᴏᴛ ᴋᴀNᴀʟı", url=SOHBET_QRUPU)],
        [InlineKeyboardButton("🛠 sᴀʜɪʙ əᴍʀɪ", callback_data="sahiba_panel")]
    ]
    
    await message.reply_photo(
        photo=SAKIL_LINKI, 
        caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- SAHİBƏ PANELİ ---
@app.on_callback_query(filters.regex("sahiba_panel"))
async def sahiba_callback(client, callback_query):
    if callback_query.from_user.id not in OWNERS:
        return await callback_query.answer("⚠️ Bu əmrdən yalniz sᴀʜɪʙ istifadə edə bilər", show_alert=True)
    
    try:
        await callback_query.message.edit_caption(
            caption=(
                "✨ **sᴀʜɪʙ ÖZƏL PANEL**\n\n"
                "📢 **Broadcast:** `/yonlendir` ilə mesaj atın.\n"
                "🚫 **Qadağa:** `/qadaga [söz]` yazaraq qadağan edin."
            ),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Geri Qayıt", callback_data="back_home")]])
        )
    except:
        await callback_query.answer("Artıq paneldəsiniz!")

@app.on_callback_query(filters.regex("back_home"))
async def back_home(client, callback_query):
    buttons = [
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("👨‍💻 sᴀʜɪʙ", url="https://t.me/Kullaniciadidi"), InlineKeyboardButton("🐦‍🔥 ʙᴏᴛ ᴋᴀNᴀʟı", url=SOHBET_QRUPU)],
        [InlineKeyboardButton("🛠 sᴀʜɪʙ əᴍʀɪ", callback_data="sahiba_panel")]
    ]
    await callback_query.message.edit_caption(
        caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- QADAGA SİSTEMİ ---
@app.on_message(filters.command("qadaga"))
async def qadaga_cmd(client, message):
    if message.from_user.id not in OWNERS:
        return await message.reply_text("⚠️ **Bu əmrdən yalniz sᴀʜɪʙə istifadə edə bilər**")
    
    if len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa qadağan ediləcək sözü yazın.")
    
    word = message.text.split(None, 1)[1].lower()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO qadaga_list (word) VALUES (%s) ON CONFLICT DO NOTHING", (word,))
    conn.commit()
    cur.close()
    conn.close()
    await message.reply_text(f"✅ **{word}** sözü qadağan olunanlara əlavə edildi.")

import os
import asyncio
import yt_dlp
import requests
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import app  #

# --- PARAMETRLƏR ---
# batbin.me-dən aldığın cookie faylını cookies.txt olaraq botun qovluğuna qoymalısan
COOKIES = "cookies.txt" 

# 1. 🔍 YOUTUBE AXTARIŞ (Ancaq /youtube yazanda işləyir)
@app.on_message(filters.command("youtube") & filters.group)
async def youtube_search(client, message):
    if len(message.command) < 2:
        return await message.reply_text("🔎 Axtarılacaq sözü yazın: `/youtube Röya`")
    
    query = " ".join(message.command[1:])
    status = await message.reply_text("🔎 YouTube-da axtarılır...")
    
    try:
        search = VideosSearch(query, limit=10)
        results = search.result()['result']
        
        if not results:
            return await status.edit_text("❌ Heç bir nəticə tapılmadı.")
        
        buttons = []
        for video in results:
            buttons.append([InlineKeyboardButton(
                f"🎬 {video['title'][:30]}...", 
                callback_query_data=f"yt_{video['id']}"
            )])
        
        await status.edit_text(
            f"📺 **'{query}' üçün nəticələr:**\n\nYükləmək istədiyiniz videonu seçin:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await status.edit_text(f"❌ Axtarış xətası: {str(e)}")

# 2. 🔗 LİNK TUTUCU (Sosial şəbəkə linki atılan kimi işə düşür)
@app.on_message(filters.regex(r"(https?://(?:www\.)?(?:instagram\.com|tiktok\.com|twitter\.com|x\.com|facebook\.com)\S+)"))
async def link_downloader(client, message):
    url = message.matches[0].group(1)
    
    buttons = [
        [InlineKeyboardButton("🎵 Mahnı (MP3)", callback_data=f"ext_mp3_{url}"),
         InlineKeyboardButton("🎥 Video (MP4)", callback_data=f"ext_mp4_{url}")]
    ]
    
    await message.reply_text(
        "🔗 Sosial şəbəkə linki aşkarlandı!\nHansı formatda yükləyim?",
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 3. 📥 YÜKLƏMƏ MOTORU (Bütün sosial şəbəkələr üçün)
@app.on_callback_query(filters.regex("^(yt_|dl_|ext_)"))
async def universal_downloader(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    # YouTube-dan gələn axtarış seçimi
    if data.startswith("yt_"):
        vid = data.split("_")[1]
        url = f"https://www.youtube.com/watch?v={vid}"
        buttons = [
            [InlineKeyboardButton("🎵 Mahnı (MP3)", callback_data=f"dl_mp3_{vid}"),
             InlineKeyboardButton("🎥 Video (MP4)", callback_data=f"dl_mp4_{vid}")]
        ]
        return await callback_query.edit_message_text("📥 Formatı seçin:", reply_markup=InlineKeyboardMarkup(buttons))

    # Yükləmə əmri
    if data.startswith("dl_") or data.startswith("ext_"):
        _, ftype, target = data.split("_", 2)
        url = f"https://www.youtube.com/watch?v={target}" if data.startswith("dl_") else target
        
        await callback_query.edit_message_text("⏳ Hazırlanır, bir az gözləyin...")
        
        ydl_opts = {
            'format': 'bestaudio/best' if ftype == 'mp3' else 'best',
            'outtmpl': f'downloads/%(title)s.%(ext)s',
            'quiet': True,
        }
        
        # Cookie faylı varsa istifadə et
        if os.path.exists(COOKIES):
            ydl_opts['cookiefile'] = COOKIES

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if ftype == "mp3":
                    await callback_query.message.reply_audio(filename, caption=f"🎵 {info.get('title', 'Mahnı')}")
                else:
                    await callback_query.message.reply_video(filename, caption=f"🎥 {info.get('title', 'Video')}")
                
                if os.path.exists(filename):
                    os.remove(filename)
                await callback_query.message.delete()
                
        except Exception as e:
            await callback_query.edit_message_text(f"❌ Yükləmə xətası: {str(e)}")

import wikipedia # Kitabxananın tanınması üçün bura əlavə etdim
import random

# --- WIKIPEDIA (Hər kəs üçün uyğunlaşdırıldı) ---
@app.on_message(filters.command("wiki", prefixes="."))
async def wikipedia_search(client, message):
    import wikipedia
    
    # Əgər komandadan sonra söz yazılmayıbsa
    if len(message.command) < 2:
        return await message.reply_text("❌ Zəhmət olmasa axtarılacaq mövzunu yazın. Məsələn: `.wiki Xəyal çox yarawqldı onu necə əldə edim 🗿`")
    
    query = " ".join(message.command[1:])
    status = await message.reply_text(f"🔍 **{query}** haqqında məlumat axtarılır...")
    
    try:
        wikipedia.set_lang("az")
        summary = wikipedia.summary(query, sentences=2)
        await status.edit_text(f"📚 **Mövzu:** `{query}`\n\n📝 **Məlumat:** {summary}")
    except wikipedia.exceptions.DisambiguationError:
        await status.edit_text(f"❌ `{query}` haqqında çoxlu nəticə var. Daha dəqiq yazın.")
    except wikipedia.exceptions.PageError:
        await status.edit_text(f"❌ `{query}` haqqında məlumat tapılmadı.")
    except Exception:
        await status.edit_text(f"❌ Xəta baş verdi.")

# --- ŞANS (Hər kəs üçün uyğunlaşdırıldı) ---
@app.on_message(filters.command("shans", prefixes="."))
async def shans_yoxla(client, message):
    import random
    faiz = random.randint(1, 100)
    # Mesajı yazan şəxsin adını çəkməklə cavab verir
    await message.reply_text(f"🎲 {message.from_user.first_name}, sənin bu günkü şansın: **%{faiz}**")
            
# --- YÖNLƏNDİRMƏ ---
@app.on_message(filters.command("yonlendir") & filters.user(OWNERS))
async def broadcast_func(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa yönləndiriləcək mesajı yazın!")
    
    status_msg = await message.reply_text("📢 Mesaj hər kəsə yönləndirilir...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM broadcast_list")
    chats = cur.fetchall()
    cur.close()
    conn.close()

    success = 0
    for chat in chats:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(chat[0])
            else:
                await client.send_message(chat[0], message.text.split(None, 1)[1])
            success += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            continue
    await status_msg.edit(f"✅ Yönləndirmə tamamlandı: {success} yerə göndərildi.")

import openai
from pyrogram import enums # "Yazır..." statusu üçün mütləqdir


    
    if message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id == (await client.get_me()).id:
            is_reply_to_me = True

    # Məntiq: Şəxsidə hər mesaja, qrupda isə reply olanda və ya təsadüfi cavab verir
    if is_private or is_reply_to_me or random.random() < 0.3:
        try:
            # Yuxarıda "Nunu yazır..." statusunu göstər
            await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
            
            # OpenAI müraciəti
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": NUNU_PROMPT},
                    {"role": "user", "content": message.text}
                ]
            )
            
            answer = response.choices[0].message.content
            if answer:
                await asyncio.sleep(1) # Daha təbii görünmək üçün 1 saniyə gözlə
                await message.reply_text(answer)
                
        except Exception as e:
            print(f"❌ OpenAI Xətası: {e}")
            
# --- HELP ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "📚 **BOTUN KOMANDALARI**\n\n"
        "🎮 **ƏYLƏNCƏLİ OYUNLAR:** /basket, /futbol, /dart, /slot, /dice\n\n"
        "🌍 **MƏLUMAT:**\n"
        "• /hava [şəhər] - Hava durumu\n"
        "• /valyuta - Günlük məzənə\n"
        "• /id - ID göstərər\n"
        "• /info - İstifadəçi məlumatı\n"
        "• /tercume [dil] - (Reply) Tərcümə edər\n"
        "• /wiki [mövzu] - Vikipediya axtarışı\n"
        "• /namaz [şəhər] - Namaz vaxtları\n\n"
        "📢 **TAĞ KOMANDALARI:**\n"
        "• /tag - Brilyant tağ\n"
        "• /utag - Emoji tağ\n"
        "• /flagtag - Bayraq tağ\n"
        "• /tektag - Təkli tağ\n\n"
        "🤫 **ETİRAFLAR:**\n"
        "• /etiraf [mesaj] - Anonim etiraf\n"
        "• /acetiraf [mesaj] - Açıq etiraf\n\n"
        "🛑 **DAYANDIRMAQ:** /tagstop\n"
        "💬 **CHATBOT:** /chatbot on/off\n"
        "🛡 **ADMİN:** /purge, /link on/off, /ping"
    )
    await message.reply_text(help_text)

# --- STATUSLAR (Deploy zamanı hamısı OFF olur) ---
chatbot_status = {}  
tag_process = {}
link_block_status = {}

# --- BU HİSSƏ KODUN ƏN YUXARISINDA OLMALIDIR ---
import google.generativeai as genai

# --- CHATBOT KOMANDASI ---
@app.on_message(filters.command("chatbot"))
async def chatbot_toggle(client, message):
    if not await is_admin(client, message): return
    if len(message.command) < 2:
        return await message.reply_text("**İstifadə:** `/chatbot on` və ya `/chatbot off`")
    
    status = message.command[1].lower()
    chat_id = message.chat.id
    
    if status == "on":
        chatbot_status[chat_id] = True
        await message.reply_text("**✅ Chatbot bu söhbət üçün aktiv edildi!**")
    elif status == "off":
        chatbot_status[chat_id] = False
        await message.reply_text("**❌ Chatbot bu söhbət üçün söndürüldü!**")


                             
# --- TAĞ SİSTEMİ (Heç nə silinmədi, yanına mesaj yazmaq özəlliyi əlavə edildi) ---
@app.on_message(filters.command(["tag", "utag", "flagtag", "tektag"]))
async def tag_handler(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("**❌ Bu komanda yalnız qruplar üçün nəzərdə tutulub!**")
    if not await is_admin(client, message):
        return
    
    chat_id = message.chat.id
    tag_process[chat_id] = True
    cmd = message.command[0]
    
    # Komandadan sonrakı mətni götürürük
    user_msg = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    await message.reply_text(f"**✅ {cmd} başladı!**")
    
    async for m in client.get_chat_members(chat_id):
        if not tag_process.get(chat_id, False):
            break
        if m.user and not m.user.is_bot:
            try:
                # Orijinal formatlar (tag, utag, flagtag, tektag) olduğu kimi qaldı
                if cmd == "tag":
                    tag_text = f"💎 [{m.user.first_name}](tg://user?id={m.user.id}) {user_msg}"
                elif cmd == "utag":
                    tag_text = f"{random.choice(EMOJILER)} [{m.user.first_name}](tg://user?id={m.user.id}) {user_msg}"
                elif cmd == "flagtag":
                    tag_text = f"{random.choice(BAYRAQLAR)} [{m.user.first_name}](tg://user?id={m.user.id}) {user_msg}"
                elif cmd == "tektag":
                    tag_text = f"👤 [{m.user.first_name}](tg://user?id={m.user.id}) {user_msg}"
                
                await client.send_message(chat_id, tag_text.strip())
                await asyncio.sleep(2.5)
            except:
                pass

@app.on_message(filters.command("tagstop") & filters.group)
async def stop_tag(client, message):
    if not await is_admin(client, message):
        return
    tag_process[message.chat.id] = False
    await message.reply_text("**🛑 Tağ dayandırıldı.**")

# --- HAVA VƏ VALYUTA (Tamamilə toxunulmaz qaldı) ---
@app.on_message(filters.command("hava"))
async def get_weather_cmd(client, message):
    if len(message.command) < 2: return await message.reply_text("🏙 Şəhər adı yazın.")
    city = message.command[1]
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid=b6907d289e10d714a6e88b30761fae22&units=metric&lang=az").json()
        await message.reply_text(f"🌤 **{city.capitalize()}**\n🌡 Temperatur: {r['main']['temp']}°C\n☁️ Vəziyyət: {r['weather'][0]['description']}")
    except: await message.reply_text("❌ Şəhər tapılmadı.")

@app.on_message(filters.command("valyuta"))
async def get_val_cmd(client, message):
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/AZN").json()
        await message.reply_text(f"💰 **Məzənnə:**\n\n🇺🇸 1 USD = {1/r['rates']['USD']:.2f} AZN\n🇪🇺 1 EUR = {1/r['rates']['EUR']:.2f} AZN")
    except: await message.reply_text("❌ Məzənnə alınmadı.")

@app.on_message(filters.command("link"))
async def link_toggle(client, message):
    if not await is_admin(client, message): return
    if len(message.command) < 2: return await message.reply_text("/link on/off")
    status = message.command[1].lower()
    link_block_status[message.chat.id] = (status == "on")
    await message.reply_text(f"🛡 Link qoruması **{status}** edildi.")

# --- ƏSAS HANDLER (History, Stats, Qadağa, Xeyal və Chatbot) ---
@app.on_message(filters.text & ~filters.bot, group=1)
async def message_handler(client, message):
    chat_id = message.chat.id
    text = message.text.lower()
    uid = message.from_user.id
    fname = message.from_user.first_name
    uname = message.from_user.username or "Yoxdur"

    # Link qoruması (Silinmədi)
    if ("http" in text or "t.me" in text) and link_block_status.get(chat_id, False):
        if not await is_admin(client, message):
            await message.delete()
            return

    conn = get_db_connection()
    cur = conn.cursor()
    
    # User History & Stats (Bütün bazaya yazma məntiqi qorundu)
    cur.execute("SELECT old_name FROM user_history WHERE user_id = %s ORDER BY date DESC LIMIT 1", (uid,))
    last = cur.fetchone()
    if not last or last[0] != fname:
        cur.execute("INSERT INTO user_history (user_id, old_name, old_username) VALUES (%s, %s, %s)", (uid, fname, uname))
    
    cur.execute("INSERT INTO user_stats (user_id, msg_count) VALUES (%s, 1) ON CONFLICT (user_id) DO UPDATE SET msg_count = user_stats.msg_count + 1", (uid,))

    # Qadağa Listi (Silinmədi)
    cur.execute("SELECT word FROM qadaga_list")
    qadagalar = [r[0] for r in cur.fetchall()]
    for word in qadagalar:
        if word in text:
            if message.from_user.id not in OWNERS:
                await message.delete()
                cur.close(); conn.close()
                return

    # --- XEYAL REAKSİYASI ---
    if "xeyal" in text or "xəyal" in text:
        try:
            await message.set_reaction(reactions=[types.ReactionTypeEmoji(emoji="🗿")])
            await message.reply_text("**istirahət ellləmmm**")
        except: pass

    # --- CHATBOT (Hər qrupa özəl və sönülü başlayır) ---
    if chatbot_status.get(chat_id, False) and not message.text.startswith('/'):
        cur.execute("INSERT INTO brain (content, chat_id) VALUES (%s, %s)", (message.text, chat_id))
        if random.random() < 0.2:
            await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
            cur.execute("SELECT content FROM brain WHERE chat_id = %s ORDER BY RANDOM() LIMIT 1", (chat_id,))
            res = cur.fetchone()
            if res: await message.reply_text(f"**{res[0]}**")
        if "bot" in text:
            await message.reply_text(f"**{random.choice(CB_SOZLER)}**")
    
    cur.close()
    conn.close()
                
# --- TƏRCÜMƏ ---
@app.on_message(filters.command("tercume") & filters.reply)
async def translate_msg(client, message):
    text = message.reply_to_message.text
    if not text: return
    
    if len(message.command) > 1:
        target_lang = message.command[1].lower()
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
            r = requests.get(url).json()
            await message.reply_text(f"🌐 **{target_lang.upper()}:**\n`{r[0][0][0]}`")
        except: await message.reply_text("❌ Xəta.")
    else:
        langs = {"en": "🇬🇧 EN", "tr": "🇹🇷 TR", "ru": "🇷🇺 RU", "de": "🇩🇪 DE", "fr": "🇫🇷 FR"}
        res = "🌐 **5 Dilə Tərcümə:**\n\n"
        for code, name in langs.items():
            try:
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={code}&dt=t&q={urllib.parse.quote(text)}"
                r = requests.get(url).json()
                res += f"🔹 {name}: `{r[0][0][0]}`\n"
            except: continue
        await message.reply_text(res)

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

# --- ŞRİFTLƏRİN LÜĞƏTİ ---
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
    if font_type == "f6": return text[::-1]
    result = ""
    font_alphabet = FONTS.get(font_type)
    for char in text.lower():
        if char in NORMAL_CHARS:
            index = NORMAL_CHARS.index(char)
            result += font_alphabet[index]
        else: result += char
    return result

@app.on_message(filters.command("font"))
async def font_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("✨ **Zəhmət olmasa mətni yazın.**\nMəsələn: `/font Salam`")
    user_text = " ".join(message.command[1:])
    buttons = [
        [InlineKeyboardButton("𝔻𝕠𝕦𝕓𝕝𝕖", callback_data=f"fn_f1"), InlineKeyboardButton("𝓢𝓬𝓻𝓲𝓹𝓽", callback_data=f"fn_f2")],
        [InlineKeyboardButton("𝔉𝔯𝔞𝔨𝔱𝔲𝔯", callback_data=f"fn_f3"), InlineKeyboardButton("Ⓒⓘⓡⓒⓛⓔⓓ", callback_data=f"fn_f4")],
        [InlineKeyboardButton("sᴍᴀʟʟ ᴄᴀᴘs", callback_data=f"fn_f5"), InlineKeyboardButton("Inverted", callback_data=f"fn_f6")],
        [InlineKeyboardButton("Gɾҽҽƙ", callback_data=f"fn_f7"), InlineKeyboardButton("คɭเєภ", callback_data=f"fn_f8")],
        [InlineKeyboardButton("卂丂丨卂几", callback_data=f"fn_f9"), InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data=f"fn_f10")],
        [InlineKeyboardButton("🅂🅀🅄🄰🅁🄴", callback_data=f"fn_f12"), InlineKeyboardButton("🅰🅱🅲", callback_data=f"fn_f13")],
        [InlineKeyboardButton("🎨 Qarışıq Stil", callback_data="fn_f1")]
    ]
    await message.reply_text(f"📝 **Mətniniz:** `{user_text}`\n✨ Stil seçin:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^fn_"))
async def font_callback(client, callback_query: CallbackQuery):
    font_id = callback_query.data.split("_")[1]
    try: original_text = callback_query.message.text.split("`")[1]
    except: return await callback_query.answer("❌ Mətn tapılmadı.")
    converted_text = font_converter(original_text, font_id)
    await callback_query.edit_message_text(f"✨ **Yeni şriftlə mətniniz:**\n\n`{converted_text}`")

# --- 💖 SEVGİ LABORATORİYASI ---
@app.on_message(filters.command("sevgi") & filters.group)
async def love_ultra_elite(client, message):
    if message.reply_to_message: target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: target = await client.get_users(message.command[1])
        except: return await message.reply_text("❌ **İstifadəçi tapılmadı!**")
    else: return await message.reply_text("💖 **Analiz üçün birinə reply atın.**")

    if target.id == message.from_user.id: return await message.reply_text("😅 Özünə eşq elan etmək?")

    status = await message.reply_text("🧪 **Analiz edilir...**")
    await asyncio.sleep(1)
    p = random.randint(0, 100)
    ehtiras, sadiqlik = random.randint(10, 100), random.randint(10, 100)
    bar = "❤️" * (p // 10) + "🖤" * (10 - (p // 10))
    
    await status.edit_text(
        f"**╔════════════════════╗**\n"
        f"** ❤️ SEVGİ HESABATI (V4)    **\n"
        f"**╚════════════════════╝**\n\n"
        f"👤 **Aşiq:** {message.from_user.first_name}\n"
        f"👤 **Məşuq:** {target.first_name}\n\n"
        f"📊 **Ümumi Uyğunluq:** `{p}%` \n"
        f"**[{bar}]**\n\n"
        f"🔥 **Ehtiras:** `{ehtiras}%` | ✅ **Sadiqlik:** `{sadiqlik}%`"
    )

# --- 👊 ŞAPALAQ (SLAP MEGA PACK) ---
@app.on_message(filters.command("slap") & filters.group)
async def slap_mega_pack(client, message):
    if message.reply_to_message: t_user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try: t_user = await client.get_users(message.command[1])
        except: return
    else: return await message.reply_text("👊 **Kimi vuraq?**")

    me = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    him = f"[{t_user.first_name}](tg://user?id={t_user.id})"

    slaps = [
        f"🧤 {me}, {him} şəxsini **Osmanlı şilləsi** ilə yerə sərdi!",
        f"👟 {me}, {him} üzünə **45 razmer yaş krossovka** tulladı!",
        f"🐟 {me}, {him} şəxsini **Xəzər nərəsi** ilə döydü!",
        f"🛋 {me}, {him} şəxsinə **qonaq otağının divanını** tulladı!",
        f"🧹 {me}, {him} şəxsini **süpürgə ilə** qovdu!",
        f"🚜 {me}, {him} şəxsininin üstündən **traktorla** keçdi!",
        f"🛸 {me}, {him} şəxsini **Marsa** fırlatdı!",
        f"🍳 {me}, {him} başına **isti tava** ilə vurdu (DANNG!)",
        f"🥊 {me}, {him} şəxsinə **Mayk Tayson** zərbəsi vurdu!",
        f"🚀 {me}, {him} şəxsini **raketlə** Aya göndərdi!",
        f"🚗 {me}, {him} şəxsini **Priusla** vurdu!",
        f"🥄 {me}, {him} şəxsini **çay qaşığı** ilə döydü!",
        f"💥 {me}, {him} şəxsini **yerlə yeksan etdi!**",
        f"🦖 {me}, {him} üstünə **ac bir T-Rex** buraxdı!",
        f"🥘 {me}, {him} başına **qazanla** vurdu!"
    ]
    await message.reply_text(random.choice(slaps))

# --- 🧠 ZEKA ÖLÇƏN ---
@app.on_message(filters.command("zeka") & filters.group)
async def zeka_olcen(client, message):
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    status = await message.reply_text("🌀 **Skan edilir...**")
    await asyncio.sleep(1)
    iq = random.randint(30, 200)
    await status.edit_text(f"🧠 **IQ Analizi:**\n👤 **İstifadəçi:** {target.first_name}\n📊 **Nəticə:** `{iq}` IQ")

# --- 🍀 GÜNÜN ŞANSI ---
@app.on_message(filters.command("sans") & filters.group)
async def day_luck(client, message):
    love, money, health = random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)
    await message.reply_text(f"🍀 **Günün Şansı:**\n❤️ Sevgi: %{love}\n💰 Pul: %{money}\n🍏 Sağlamlıq: %{health}")

# --- WİKİPEDİA ---
@app.on_message(filters.command("wiki"))
async def wiki_cmd(client, message):
    if len(message.command) < 2:
        return
    
    wikipedia.set_lang("az")
    try:
        # Mesajdan axtarış sözünü götürür (komandadan sonrakı hissə)
        search_query = message.text.split(None, 1)[1]
        
        # Wikipedia-dan 2 cümləlik xülasə çəkir
        summary = wikipedia.summary(search_query, sentences=2)
        
        await message.reply_text(f"📖 {summary}")
        
    except Exception:
        # Tapılmadıqda və ya xəta olduqda
        await message.reply_text("❌ Tapılmadı.")
        
# --- NAMAZ VAXTLARI (SƏNİN İMPORTLARINLA) ---
@app.on_message(filters.command("namaz"))
async def namaz_vaxtlari(client, message):
    # Əgər şəhər yazılmayıbsa Bakı götürür
    city = message.command[1] if len(message.command) > 1 else "Baku"
    
    try:
        # Namaz vaxtları API
        url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Azerbaijan&method=3"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        r = requests.get(url, headers=headers, timeout=10).json()
        
        if 'data' not in r:
            return await message.reply_text("❌ Şəhər tapılmadı (İngiliscə yazın. Məs: /namaz Ganja)")
            
        t = r['data']['timings']
        
        # Səliqəli format
        res = (
            f"🕋 **{city.capitalize()} Namaz Vaxtları**\n\n"
            f"🌅 Sübh: `{t['Fajr']}`\n"
            f"☀️ Günəş: `{t['Sunrise']}`\n"
            f"🕛 Zöhr: `{t['Dhuhr']}`\n"
            f"🕒 Əsr: `{t['Asr']}`\n"
            f"🌇 Axşam: `{t['Maghrib']}`\n"
            f"🌃 İşа: `{t['Isha']}`"
        )
        await message.reply_text(res)
        
    except Exception:
        await message.reply_text("⚠️ Namaz vaxtlarını gətirmək mümkün olmadı.")                        
# --- ETİRAF TƏSDİQ SİSTEMİ (YENİ) ---
@app.on_message(filters.command(["etiraf", "acetiraf"]))
async def etiraf_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Zəhmət olmasa etirafınızı yazın.")
    
    is_anon = "Anonim" if message.command[0] == "etiraf" else f"Açıq ({message.from_user.mention})"
    etiraf_text = message.text.split(None, 1)[1]
    
    # Sahibəyə düymələr göndərilir
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Təsdiqlə", callback_data=f"approve_etiraf|{message.chat.id}"),
            InlineKeyboardButton("❌ Rədd et", callback_data="decline_etiraf")
        ]
    ])
    
    await client.send_message(
        SAHIBE_ID, 
        f"🔔 **Yeni Etiraf Gəldi!**\n\n**Növ:** {is_anon}\n**Etiraf:**\n`{etiraf_text}`",
        reply_markup=keyboard
    )
    await message.reply_text("✅ Etirafınız sahibəyə göndərildi. Təsdiq edildikdən sonra paylaşılacaq.")

@app.on_callback_query(filters.regex(r"^(approve_etiraf|decline_etiraf)"))
async def process_etiraf_callback(client, callback_query):
    if callback_query.from_user.id != SAHIBE_ID:
        return await callback_query.answer("Sən sahibə deyilsən!", show_alert=True)
    
    action = callback_query.data.split("|")[0]
@app.on_callback_query(filters.regex(r"^(approve_etiraf|decline_etiraf)"))
async def process_etiraf_callback(client, callback_query):
    if callback_query.from_user.id != SAHIBE_ID:
        return await callback_query.answer("Sən sahibə deyilsən!", show_alert=True)

    # 410-cu sətir - İndi funksiyanın daxilindədir
    action = callback_query.data.split("|")[0]

    if action == "approve_etiraf":
        # Etiraf mətnini mesajdan çıxarırıq
        et_msg = callback_query.message.text.split("Etiraf:\n")[1]
        header = "🤫 **Anonim Etiraf**" if "Anonim" in callback_query.message.text else "📢 **Açıq Etiraf**"
        
        # Qrupa göndər
        qrup_user = SOHBET_QRUPU.split('/')[-1]
        await client.send_message(qrup_user, f"{header}:\n\n`{et_msg}`")
        await callback_query.message.edit_text("✅ Etiraf təsdiqləndi və qrupda paylaşıldı.")
        
    elif action == "decline_etiraf":
        await callback_query.message.edit_text("❌ Etiraf rədd edildi.")

# --- OYUNLAR VƏ MƏLUMAT SİSTEMİ ---
@app.on_message(filters.command(["basket", "futbol", "dart", "slot", "dice"]))
async def games_handler(client, message):
    icons = {"basket": "🏀", "futbol": "⚽", "dart": "🎯", "slot": "🎰", "dice": "🎲"}
    cmd = message.command[0]
    await client.send_dice(message.chat.id, icons.get(cmd, "🎲"))

@app.on_message(filters.command("id"))
async def get_id(client, message):
    user = message.from_user
    text = f"👤 **İstifadəçi:** {user.first_name}\n🆔 **ID:** `{user.id}`\n"
    if message.chat.type != ChatType.PRIVATE:
        text += f"👥 **Qrup ID:** `{message.chat.id}`"
    await message.reply_text(text)

@app.on_message(filters.command("info"))
async def user_info(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    status = await client.get_chat_member(message.chat.id, user.id)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT msg_count FROM user_stats WHERE user_id = %s", (user.id,))
    stats = cur.fetchone()
    msg_count = stats[0] if stats else 0
    cur.close(); conn.close()

    # 445-ci sətirdəki xətanın düzəldilmiş forması (Multi-line string)
    text = (
        f"📋 **İstifadəçi Məlumatı:**\n"
        f"• Ad: {user.first_name}\n"
        f"• ID: `{user.id}`\n"
        f"• Status: {status.status}\n"
        f"• Mesaj Sayı: {msg_count}"
    )
    await message.reply_text(text)

# --- BOTUN İŞƏ SALINMASI ---
async def main():
    async with app:
        # Pluginləri yükləyirik
        load_plugins(app)
        
        # 467-ci sətir: set_bot_commands (hərf səhvini düzəltdim)
        await app.set_bot_commands([
            BotCommand("start", "Botu başladın"),
            BotCommand("help", "Kömək menyusu"),
            BotCommand("tag", "Brilyant tağ"),
            BotCommand("etiraf", "Anonim etiraf"),
            BotCommand("basket", "Basketbol"),
            BotCommand("futbol", "Futbol"),
            BotCommand("slot", "Kazino"),
            BotCommand("id", "ID göstər"),
            BotCommand("info", "Məlumat"),
            BotCommand("masinlar", "Maşın kataloqu"),
            BotCommand("sevgi", "Sevgi testi"),
            BotCommand("zeka", "Zəka ölçən"),
            BotCommand("sans", "Günün şansı"),
            BotCommand("slap", "Şillə vurmaq"),
            BotCommand("font", "Şrift dəyişdirici")
        ])
        
        print("🚀 Bot aktivdir və oyunlar yükləndi!")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    try:
        # Əsas düzəliş budur: app.run() yerinə app.run(main()) 
        app.run(main())
    except KeyboardInterrupt:
        pass
