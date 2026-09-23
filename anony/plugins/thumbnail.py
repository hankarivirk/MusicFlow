from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.helpers._admins import is_admin
from anony.utils.database import is_thumb_enabled, set_thumb, set_global_thumb
import config

@app.on_message(filters.command(["thumb", "thumbnail"]) & filters.group)
async def group_thumb_toggle(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    
    if len(message.command) < 2:
        current = await is_thumb_enabled(message.chat.id)
        status = "**Enabled** (Photo)" if current else "**Disabled** (Fast Text-Only)"
        return await message.reply_text(
            f"**Group Thumbnail Status:** {status}\n\n"
            f"Toggle with: `/thumb on` or `/thumb off`"
        )
    
    arg = message.command[1].lower()
    if arg in ["on", "enable", "yes", "true"]:
        await set_thumb(message.chat.id, True)
        await message.reply_text("✅ **Thumbnails Enabled** for this group.")
    elif arg in ["off", "disable", "no", "false"]:
        await set_thumb(message.chat.id, False)
        await message.reply_text("⚡ **Thumbnails Disabled** (Fast Text-Only Mode) for this group.")
    else:
        await message.reply_text("Usage: `/thumb on` or `/thumb off`")

@app.on_message(filters.command(["globalthumb", "gthumb"]) & filters.user(config.OWNER_ID))
async def owner_global_thumb(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/globalthumb on` or `/globalthumb off`")
    
    arg = message.command[1].lower()
    if arg in ["on", "enable", "true"]:
        await set_global_thumb(True)
        await message.reply_text("🌐 **Global Default:** Thumbnails are now **ON** by default.")
    elif arg in ["off", "disable", "false"]:
        await set_global_thumb(False)
        await message.reply_text("🌐 **Global Default:** Thumbnails are now **OFF** (Text-Only) by default.")
    else:
        await message.reply_text("Usage: `/globalthumb on` or `/globalthumb off`")
