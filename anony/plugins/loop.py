from pyrogram import filters
from pyrogram.types import Message
from anony import app
from anony.core.calls import MusicCall
from anony.helpers._admins import is_admin

@app.on_message(filters.command("loop") & filters.group)
async def loop_cmd(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("🔒 Admin only command.")
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/loop <1-10>` or `/loop disable`")
    
    arg = message.command[1].lower()
    if arg in ["disable", "off", "0"]:
        MusicCall.loops[message.chat.id] = 0
        return await message.reply_text("🔁 **Loop disabled.**")
    
    if arg.isdigit() and 1 <= int(arg) <= 10:
        MusicCall.loops[message.chat.id] = int(arg)
        return await message.reply_text(f"🔁 **Loop enabled for {arg} times.**")
    
    await message.reply_text("❌ Please enter a number between 1 and 10.")
