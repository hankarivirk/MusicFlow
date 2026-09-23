from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.utils.database import set_lang, get_lang
from anony.helpers._admins import is_admin

@app.on_message(filters.command(["lang", "language"]) & filters.group)
async def lang_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if len(message.command) < 2:
        current = await get_lang(message.chat.id)
        return await message.reply_text(
            f"Current language: `{current}`\n\n"
            f"Available options: `/lang en` (English), `/lang hi` (Hindi)"
        )
    target = message.command[1].lower()
    if target in ["en", "hi"]:
        await set_lang(message.chat.id, target)
        await message.reply_text(f"✅ Language changed to `{target}`.")
    else:
        await message.reply_text("❌ Supported languages are `en` and `hi`.")
