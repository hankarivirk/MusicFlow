from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.utils.database import is_sudo

@app.on_message(filters.command(["activevc", "activevoice"]) & filters.private)
async def active_vc_cmd(_, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    active_chats = list(MusicCall.active_tracks.keys())
    if not active_chats:
        return await message.reply_text("No active voice chats.")
    text = f"**Active Voice Chats ({len(active_chats)}):**\n\n"
    for cid in active_chats:
        text += f"• `{cid}`\n"
    await message.reply_text(text)
