from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from anony import app
from anony.core.youtube import YouTube
from anony.helpers._inline import recommendation_markup
from anony.utils.database import set_autoplay, is_autoplay, is_blacklisted

@app.on_message(filters.command("autoplay") & filters.group)
async def toggle_autoplay(_, message: Message):
    if await is_blacklisted(message.chat.id):
        return
    chat_id = message.chat.id
    current = await is_autoplay(chat_id)
    new_state = not current
    await set_autoplay(chat_id, new_state)
    
    status = "**Enabled** ⚡" if new_state else "**Disabled** ❌"
    await message.reply_text(
        f"**AutoPlay Mode:** {status}\n\n"
        f"When enabled, Music Flow automatically plays related songs when the queue ends."
    )

@app.on_callback_query(filters.regex(r"^rec_play_"))
async def play_recommended(_, query: CallbackQuery):
    video_id = query.data.split("_")[2]
    await query.answer("Playing selected track...")
    from anony.plugins.play import play_track_url
    await play_track_url(query.message, f"https://www.youtube.com/watch?v={video_id}")

@app.on_callback_query(filters.regex(r"^rec_more_"))
async def more_recommendations(_, query: CallbackQuery):
    _, _, base_vid, offset = query.data.split("_")
    offset = int(offset)
    recs = await YouTube.get_recommendations(base_vid, limit=12)
    if not recs:
        return await query.answer("No more songs found.", show_alert=True)
    
    markup = recommendation_markup(recs, base_vid, offset)
    await query.edit_message_reply_markup(reply_markup=markup)
