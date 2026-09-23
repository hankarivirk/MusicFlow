import time
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from anony import app
import config

@app.on_message(filters.command(["ping"]))
async def ping_pong(_, message: Message):
    start = time.time()
    msg = await message.reply_text("⚡ Checking ping...")
    latency = round((time.time() - start) * 1000)
    
    text = (
        f"**{config.BOT_NAME} System Status**\n\n"
        f"• **Ping:** `{latency} ms`\n"
        f"• **Engine:** `PyTgCalls`\n"
        f"• **Stream:** `Fast Mode`"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="📢 Channel", url=config.SUPPORT_CHANNEL)]
    ])
    await msg.edit_text(text, reply_markup=buttons)
