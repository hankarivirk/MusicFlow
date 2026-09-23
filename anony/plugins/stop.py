from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._queue import Queues
from anony.helpers._admins import is_admin

@app.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    chat_id = message.chat.id
    if not MusicCall.call:
        return
    try:
        await MusicCall.call.leave_group_call(chat_id)
        MusicCall.active_tracks.pop(chat_id, None)
        Queues.clear_queue(chat_id)
        await message.reply_text("⏹ **Playback stopped and queue cleared.**")
    except Exception:
        await message.reply_text("❌ Not currently in voice chat.")
