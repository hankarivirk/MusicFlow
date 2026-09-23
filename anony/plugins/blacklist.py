from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.utils.database import blacklist_chat, whitelist_chat
import config

@app.on_message(filters.command("blacklistchat") & filters.user(config.OWNER_ID))
async def bl_chat(_, message: Message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.command[1])
    await blacklist_chat(chat_id)
    await message.reply_text(f"🚫 Chat `{chat_id}` has been blacklisted.")

@app.on_message(filters.command("whitelistchat") & filters.user(config.OWNER_ID))
async def wl_chat(_, message: Message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.command[1])
    await whitelist_chat(chat_id)
    await message.reply_text(f"✅ Chat `{chat_id}` has been whitelisted.")
