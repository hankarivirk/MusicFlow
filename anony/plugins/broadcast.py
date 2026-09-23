import asyncio
from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.utils.database import is_sudo
from anony.core.mongo import mongodb

@app.on_message(filters.command(["broadcast", "gcast"]))
async def broadcast_cmd(_, message: Message):
    if not await is_sudo(message.from_user.id):
        return
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast.")
    
    sent = 0
    status = await message.reply_text("📢 Starting broadcast...")
    if mongodb is not None:
        try:
            cursor = mongodb.chats.find()
            async for doc in cursor:
                try:
                    await message.reply_to_message.copy(doc["chat_id"])
                    sent += 1
                    await asyncio.sleep(0.1)
                except Exception:
                    pass
        except Exception:
            pass
    await status.edit_text(f"📢 Broadcast completed. Sent to `{sent}` chats.")
