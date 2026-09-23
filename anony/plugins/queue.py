from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from anony import app
from anony.helpers._queue import Queues
from anony.helpers._telegraph import create_telegraph_queue_page
import config

@app.on_message(filters.command(["queue", "q"]) & filters.group)
async def queue_cmd(_, message: Message):
    q = Queues.get_queue(message.chat.id)
    if not q:
        return await message.reply_text("📋 Queue is empty.")
    
    total = len(q)
    text = f"📋 **Upcoming Queue ({total} tracks):**\n\n"
    
    # Show first 10 tracks in chat
    for i, t in enumerate(q[:10], 1):
        text += f"{i}. [{t['title']}]({t['link']}) | `{t['duration']}`\n"
    
    buttons = []
    if total > 10:
        text += f"\n*...and {total - 10} more tracks in queue.*"
        # Generate Telegraph webpage view for long queues
        t_url = await create_telegraph_queue_page(message.chat.title or "Group", q)
        if t_url:
            buttons.append([
                InlineKeyboardButton(text=f"🌐 View Full Queue on Telegraph ({total})", url=t_url)
            ])

    buttons.append([
        InlineKeyboardButton(text="📢 Channel", url=config.SUPPORT_CHANNEL)
    ])
    
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
