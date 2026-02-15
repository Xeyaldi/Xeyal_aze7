from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot.py-dakı dəyişənləri bura da tanıtmış oluruq
SAKIL_LINKI = "https://i.postimg.cc/mDTTvtxS/20260214-163714.jpg" 
SOHBET_QRUPU = "https://t.me/sohbetqruprc" 

def init_start(app):
    @app.on_message(filters.command("start"))
    async def start_cmd(client, message):
        # Düymələr
        buttons = [
            [
                InlineKeyboardButton(
                    "➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", 
                    url=f"https://t.me/{(await client.get_me()).username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), 
                InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)
            ],
            [
                InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")
            ]
        ]
        
        # Şəkilli mesajın göndərilməsi
        await message.reply_photo(
            photo=SAKIL_LINKI, 
            caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Bot.py-dakı "back_home" düyməsinə basanda start mesajına qayıtmaq üçün əlavə
    @app.on_callback_query(filters.regex("back_home"))
    async def back_home(client, callback_query):
        buttons = [
            [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴜɴᴜᴢᴀ əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton("👩‍💻 sᴀʜɪʙə", url="https://t.me/Aysberqqq"), InlineKeyboardButton("💬 sÖʜʙəᴛ ǫʀᴜᴘᴜ", url=SOHBET_QRUPU)],
            [InlineKeyboardButton("🛠 sᴀʜɪʙə əᴍʀɪ", callback_data="sahiba_panel")]
        ]
        await callback_query.message.edit_caption(
            caption="**sᴀʟᴀᴍ ! ᴍəɴ ᴘʀᴏғᴇssɪᴏɴᴀʟ ᴛᴀɢ ᴠə ᴄʜᴀᴛʙᴏᴛ ʙᴏᴛᴜʏᴀᴍ.**\n\n**ᴋᴏᴍᴜᴛʟᴀʀ üçüɴ /help ʏᴀᴢıɴ.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
