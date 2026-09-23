from pyrogram import filters
from pyrogram.types import Message
from anony import app
import config

@app.on_message(filters.command(["help"]))
async def help_cmd(_, message: Message):
    text = (
        f"**{config.BOT_NAME} Commands Manual:**\n\n"
        f"**Playback Controls:**\n"
        f"• `/play <song or link>`: Stream audio in voice chat\n"
        f"• `/playlist <playlist/mix link>`: Enqueue full YouTube Playlist or My Mix\n"
        f"• `/vplay <song>`: Stream video in voice chat\n"
        f"• `/pause`: Pause playback\n"
        f"• `/resume`: Resume stream\n"
        f"• `/skip`: Skip to next song\n"
        f"• `/stop`: Stop stream & clear queue\n"
        f"• `/autoplay`: Toggle continuous recommendations\n"
        f"• `/volume <1-200>`: Adjust voice chat volume\n"
        f"• `/loop <1-10>`: Repeat current song\n"
        f"• `/seek <sec>`: Seek forward in song\n"
        f"• `/queue`: View upcoming tracks in queue\n\n"
        f"**Group Customization:**\n"
        f"• `/thumb <on|off>`: Toggle YouTube thumbnails (Photo/Text-only)\n"
        f"• `/cleanmode <on|off>`: Toggle auto-delete chat cleaner\n"
        f"• `/auth` & `/unauth`: Manage music rights for users\n\n"
        f"**System & Status:**\n"
        f"• `/ping`: Check bot response latency\n"
        f"• `/stats`: Server performance & uptime\n\n"
        f"**Official Channel:** {config.SUPPORT_CHANNEL}"
    )
    await message.reply_text(text)
