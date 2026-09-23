from pyrogram import filters
from pyrogram.types import Message
from anony import app
import config
from anony.helpers._inline import start_panel
from anony.utils.database import is_blacklisted

@app.on_message(filters.command(["start"]) & filters.private)
async def start_private(_, message: Message):
    text = (
        f"Hey {message.from_user.mention},\n\n"
        f"Welcome to **{config.BOT_NAME}** ✨\n\n"
        f"A fast, high-quality music streaming bot for Telegram voice chats.\n\n"
        f"• **Latency:** Low buffer\n"
        f"• **AutoPlay:** Supported\n\n"
        f"Add me to your group to start listening."
    )
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=text,
        reply_markup=start_panel()
    )

@app.on_message(filters.command(["start"]) & filters.group)
async def start_group(_, message: Message):
    if await is_blacklisted(message.chat.id):
        return
    await message.reply_text(
        f"**{config.BOT_NAME} is active in this group.** ✨\n\n"
        f"Use `/play <song name>` to stream music."
    )
