from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from anony import app
from anony.core.calls import MusicCall
from anony.core.youtube import YouTube
from anony.helpers._inline import stream_markup
from anony.helpers._queue import Queues
from anony.helpers._play import get_stream_url
from anony.helpers._telegraph import create_telegraph_queue_page
from anony.utils.database import is_blacklisted, is_thumb_enabled
import config

async def play_track_url(message: Message, link: str):
    chat_id = message.chat.id
    track = await YouTube.search(link)
    if not track:
        return await message.reply_text("❌ Could not load track.")
    
    track["stream_url"] = await get_stream_url(track["link"])
    track["requester"] = message.from_user.mention if message.from_user else "Anonymous"
    
    if not MusicCall.active_tracks.get(chat_id):
        await MusicCall.play(chat_id, track)
        text = (
            f"🎵 **Now Playing:** [{track['title']}]({track['link']})\n"
            f"• **Duration:** `{track['duration']}`\n"
            f"• **Requested by:** {track['requester']}"
        )
        if await is_thumb_enabled(chat_id) and track.get("thumb"):
            await message.reply_photo(
                photo=track["thumb"],
                caption=text,
                reply_markup=stream_markup(chat_id)
            )
        else:
            await message.reply_text(
                text=text,
                reply_markup=stream_markup(chat_id)
            )
    else:
        Queues.add_to_queue(chat_id, track)
        await message.reply_text(
            f"📋 **Added to Queue:** [{track['title']}]({track['link']})"
        )

@app.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play_cmd(_, message: Message):
    if await is_blacklisted(message.chat.id):
        return
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/play <song name, playlist link, or mix link>`")
    
    query = message.text.split(None, 1)[1]
    requester = message.from_user.mention if message.from_user else "Anonymous"
    chat_id = message.chat.id

    # Detect YouTube Playlists, YouTube Mixes (RD...), My Mix (RDMM...), etc.
    if "list=" in query or "playlist" in query:
        status_msg = await message.reply_text("⚡ **Fetching Playlist / Mix...**")
        pl_title, tracks = await YouTube.get_playlist(query, limit=config.PLAYLIST_FETCH_LIMIT)
        if not tracks:
            return await status_msg.edit_text("❌ Could not fetch playlist or it is private/empty.")

        await status_msg.edit_text(f"⚡ **Loaded {len(tracks)} tracks from:** `{pl_title}`")
        
        for t in tracks:
            t["requester"] = requester

        # Telegraph URL for long playlists
        t_url = None
        if len(tracks) > 10:
            t_url = await create_telegraph_queue_page(pl_title, tracks)

        if not MusicCall.active_tracks.get(chat_id):
            first_track = tracks[0]
            first_track["stream_url"] = await get_stream_url(first_track["link"])
            await MusicCall.play(chat_id, first_track)

            for remaining in tracks[1:]:
                Queues.add_to_queue(chat_id, remaining)

            text = (
                f"🎵 **Now Playing Playlist:** [{pl_title}]({query})\n"
                f"• **Current Track:** [{first_track['title']}]({first_track['link']})\n"
                f"• **Total Enqueued:** `{len(tracks)} tracks`\n"
                f"• **Requested by:** {requester}"
            )
            await status_msg.delete()
            markup = stream_markup(chat_id)
            if t_url:
                markup.inline_keyboard.insert(0, [
                    InlineKeyboardButton(text=f"🌐 View All {len(tracks)} Tracks on Telegraph", url=t_url)
                ])

            if await is_thumb_enabled(chat_id) and first_track.get("thumb"):
                await message.reply_photo(
                    photo=first_track["thumb"],
                    caption=text,
                    reply_markup=markup
                )
            else:
                await message.reply_text(
                    text=text,
                    reply_markup=markup
                )
        else:
            queue_start = len(Queues.get_queue(chat_id)) + 1
            for t in tracks:
                Queues.add_to_queue(chat_id, t)
            
            buttons = []
            if t_url:
                buttons.append([
                    InlineKeyboardButton(text=f"🌐 View All {len(tracks)} Tracks on Telegraph", url=t_url)
                ])
            buttons.append([InlineKeyboardButton(text="📢 Channel", url=config.SUPPORT_CHANNEL)])
            
            await status_msg.edit_text(
                f"📋 **Added Playlist to Queue:** [{pl_title}]({query})\n"
                f"• **Total Tracks Added:** `{len(tracks)}`\n"
                f"• **Queue Starts At:** `#{queue_start}`",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        return

    # Single track play
    status_msg = await message.reply_text("⚡ Searching track...")
    track = await YouTube.search(query)
    if not track:
        return await status_msg.edit_text("❌ Song not found.")
    
    await status_msg.edit_text(f"⚡ Streaming `{track['title']}`...")
    track["stream_url"] = await get_stream_url(track["link"])
    track["requester"] = requester
    
    if not MusicCall.active_tracks.get(chat_id):
        await MusicCall.play(chat_id, track)
        text = (
            f"🎵 **Now Playing:** [{track['title']}]({track['link']})\n"
            f"• **Duration:** `{track['duration']}`\n"
            f"• **Requested by:** {track['requester']}"
        )
        await status_msg.delete()
        if await is_thumb_enabled(chat_id) and track.get("thumb"):
            await message.reply_photo(
                photo=track["thumb"],
                caption=text,
                reply_markup=stream_markup(chat_id)
            )
        else:
            await message.reply_text(
                text=text,
                reply_markup=stream_markup(chat_id)
            )
    else:
        Queues.add_to_queue(chat_id, track)
        await status_msg.edit_text(
            f"📋 **Added to Queue:** [{track['title']}]({track['link']})"
        )
