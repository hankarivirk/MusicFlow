from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.utils.database import add_sudo, remove_sudo
import config

@app.on_message(filters.command("addsudo") & filters.user(config.OWNER_ID))
async def add_sudo_cmd(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give an ID.")
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.command[1])
    await add_sudo(user_id)
    await message.reply_text(f"✅ Added `{user_id}` to Sudo Users.")

@app.on_message(filters.command("delsudo") & filters.user(config.OWNER_ID))
async def del_sudo_cmd(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give an ID.")
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.command[1])
    await remove_sudo(user_id)
    await message.reply_text(f"❌ Removed `{user_id}` from Sudo Users.")
