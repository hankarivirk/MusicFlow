from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._admins import is_admin

@app.on_message(filters.command("resume") & filters.group)
async def resume_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if not MusicCall.call:
        return
    try:
        await MusicCall.call.resume_stream(message.chat.id)
        await message.reply_text("▶️ **Track resumed.**")
    except Exception:
        await message.reply_text("❌ Stream is not paused.")
