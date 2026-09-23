from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.helpers._admins import is_admin

_auth_users = {}

@app.on_message(filters.command("auth") & filters.group)
async def auth_user(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to authorize them.")
    user_id = message.reply_to_message.from_user.id
    _auth_users.setdefault(message.chat.id, set()).add(user_id)
    await message.reply_text(f"✅ Authorized {message.reply_to_message.from_user.mention}.")

@app.on_message(filters.command("unauth") & filters.group)
async def unauth_user(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to unauthorize them.")
    user_id = message.reply_to_message.from_user.id
    _auth_users.get(message.chat.id, set()).discard(user_id)
    await message.reply_text(f"❌ Unauthorized {message.reply_to_message.from_user.mention}.")
