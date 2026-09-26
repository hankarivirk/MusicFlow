# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow


from pyrogram import filters, types
import aiohttp

from musicflow import app, config, db, lang, queue, thumb
from musicflow.helpers import Track, buttons

_telegraph_token = None



async def _telegraph_queue(title: str, lines: list[str]) -> str | None:
    global _telegraph_token
    content = "<p>" + "</p><p>".join(lines) + "</p>"
    try:
        async with aiohttp.ClientSession() as session:
            if not _telegraph_token:
                async with session.post(
                    "https://api.telegra.ph/createAccount",
                data={"short_name": "MusicFlow", "author_name": "MusicFlow"},
                ) as account_resp:
                    account = await account_resp.json(content_type=None)
                _telegraph_token = account.get("result", {}).get("access_token")
            if not _telegraph_token:
                return None
            async with session.post(
                "https://api.telegra.ph/createPage",
                data={"access_token": _telegraph_token, "title": title, "author_name": "MusicFlow", "content": content, "return_content": "false"},
            ) as resp:
                data = await resp.json(content_type=None)
                if data.get("ok") and data.get("result", {}).get("url"):
                    return data["result"]["url"]
    except Exception:
        return None
    return None

@app.on_message(filters.command(["queue", "playing"]) & filters.group & ~app.bl_users)
@lang.language()
async def _queue_func(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    _reply = await m.reply_text(m.lang["queue_fetching"])
    _queue = queue.get_queue(m.chat.id)
    _media = _queue[0]
    _thumb = (
        await thumb.generate(_media)
        if isinstance(_media, Track)
        else config.DEFAULT_THUMB
    ) if config.THUMB_GEN else None
    _text = m.lang["queue_curr"].format(
        _media.url,
        _media.title[:50],
        _media.duration,
        _media.user,
    )
    _queue.pop(0)

    if _queue:
        if len(_queue) > 15:
            lines = [f"<b>{i + 1}.</b> {media.title} — {media.duration}" for i, media in enumerate(_queue)]
            url = await _telegraph_queue(f"{m.chat.title} — MusicFlow Queue", lines)
            if url:
                _text += f"\n\n<b>{len(_queue)} tracks are queued.</b>\n<a href=\"{url}\">View the full queue</a>"
            else:
                _text += "<blockquote expandable>"
                for i, media in enumerate(_queue[:15], start=1):
                    _text += m.lang["queue_item"].format(i + 1, media.title, media.duration)
                _text += f"</blockquote>\n\n<b>{len(_queue) - 15} more tracks are queued.</b>"
        else:
            _text += "<blockquote expandable>"
            for i, media in enumerate(_queue, start=1):
                _text += m.lang["queue_item"].format(i + 1, media.title, media.duration)
            _text += "</blockquote>"

    _playing = await db.playing(m.chat.id)
    _buttons = buttons.queue_markup(
            m.chat.id,
            m.lang["playing"] if _playing else m.lang["paused"],
            _playing,
        )
    if thumb:
        await _reply.edit_media(
            media=types.InputMediaPhoto(
                media=_thumb,
                caption=_text,
            ),
            reply_markup=_buttons,
        )
    else:
        await _reply.edit_text(
            text=_text,
            reply_markup=_buttons,
        )
