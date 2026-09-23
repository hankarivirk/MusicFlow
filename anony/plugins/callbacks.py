from pyrogram import filters
from pyrogram.types import CallbackQuery
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._queue import Queues

@app.on_callback_query(filters.regex(r"^cb_"))
async def callbacks_handler(_, query: CallbackQuery):
    data = query.data.split("_")
    action = data[1]
    chat_id = int(data[2])

    if action == "pause":
        try:
            await MusicCall.call.pause_stream(chat_id)
            await query.answer("Paused.")
        except Exception:
            await query.answer("Error pausing track.", show_alert=True)
    elif action == "resume":
        try:
            await MusicCall.call.resume_stream(chat_id)
            await query.answer("Resumed.")
        except Exception:
            await query.answer("Error resuming track.", show_alert=True)
    elif action == "skip":
        await MusicCall.on_song_end(chat_id)
        await query.answer("Skipped track.")
    elif action == "stop":
        try:
            await MusicCall.call.leave_group_call(chat_id)
            MusicCall.active_tracks.pop(chat_id, None)
            Queues.clear_queue(chat_id)
            await query.answer("Stopped.")
            await query.message.edit_text("⏹ **Playback stopped.**")
        except Exception:
            await query.answer("Error stopping stream.", show_alert=True)
