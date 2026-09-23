from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.plugins.play import play_cmd

@app.on_message(filters.command(["playlist", "mix"]) & filters.group)
async def playlist_direct_cmd(client, message: Message):
    """Direct alias to fetch and play YouTube Playlists or My Mix collections"""
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage: `/playlist <youtube playlist link or mix link>`\n\n"
            "Example: `/playlist https://www.youtube.com/playlist?list=PL...`"
        )
    await play_cmd(client, message)
