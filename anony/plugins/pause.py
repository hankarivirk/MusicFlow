from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._admins import is_admin

@app.on_message(filters.command("pause") & filters.group)
async def pause_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if not MusicCall.call:
        return
    try:
        await MusicCall.call.pause_stream(message.chat.id)
        await message.reply_text("⏸ **Track paused.**")
    except Exception:
        await message.reply_text("❌ Nothing is currently playing.")
