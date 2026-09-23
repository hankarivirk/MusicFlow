import asyncio
from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.helpers._admins import is_admin
from anony.utils.database import is_cleanmode, set_cleanmode

@app.on_message(filters.command("cleanmode") & filters.group)
async def cleanmode_toggle(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    
    if len(message.command) < 2:
        current = await is_cleanmode(message.chat.id)
        status = "**Enabled**" if current else "**Disabled**"
        return await message.reply_text(
            f"**CleanMode Status:** {status}\n\n"
            f"Toggle with: `/cleanmode on` or `/cleanmode off`"
        )
    
    arg = message.command[1].lower()
    if arg in ["on", "enable", "true"]:
        await set_cleanmode(message.chat.id, True)
        await message.reply_text("🧹 **CleanMode Enabled.** Bot messages will auto-clear to keep chat tidy.")
    elif arg in ["off", "disable", "false"]:
        await set_cleanmode(message.chat.id, False)
        await message.reply_text("🧹 **CleanMode Disabled.**")
    else:
        await message.reply_text("Usage: `/cleanmode on` or `/cleanmode off`")

async def auto_clean_message(msg: Message, delay: int = 180):
    """Background helper to delete command messages after a few minutes"""
    if await is_cleanmode(msg.chat.id):
        await asyncio.sleep(delay)
        try:
            await msg.delete()
        except Exception:
            pass
