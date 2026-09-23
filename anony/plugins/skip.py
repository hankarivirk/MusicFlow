from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._admins import is_admin

@app.on_message(filters.command("skip") & filters.group)
async def skip_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    await MusicCall.on_song_end(message.chat.id)
    await message.reply_text("⏭ **Skipped track.**")
