import psutil
import time
from pyrogram import filters
from pyrogram.types import Message
from anony import app
import config

_boot_time = time.time()

@app.on_message(filters.command("stats"))
async def stats_cmd(_, message: Message):
    uptime = int(time.time() - _boot_time)
    m, s = divmod(uptime, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    
    text = (
        f"**{config.BOT_NAME} Server Statistics** ✨\n\n"
        f"• **Uptime:** `{d}d {h}h {m}m {s}s`\n"
        f"• **CPU Usage:** `{cpu}%`\n"
        f"• **RAM Usage:** `{ram}%`\n"
        f"• **Channel:** [Official Updates]({config.SUPPORT_CHANNEL})"
    )
    await message.reply_photo(photo=config.STATS_IMG_URL, caption=text)
