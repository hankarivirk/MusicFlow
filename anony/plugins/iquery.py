from pyrogram import filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from anony import app
from youtubesearchpython import VideosSearch
import asyncio

@app.on_inline_query()
async def inline_search(_, query: InlineQuery):
    text = query.query.strip()
    if not text:
        return
    try:
        search = VideosSearch(text, limit=5)
        result = await asyncio.to_thread(search.result)
        results = []
        for track in result.get("result", []):
            results.append(
                InlineQueryResultArticle(
                    title=track.get("title"),
                    input_message_content=InputTextMessageContent(
                        f"🎵 /play {track.get('link')}"
                    ),
                    description=track.get("duration"),
                    thumb_url=track.get("thumbnails", [{}])[0].get("url"),
                )
            )
        await query.answer(results)
    except Exception:
        pass
