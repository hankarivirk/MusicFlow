import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from anony import app
from anony.core.userbot import userbot
from anony.core.youtube import YouTube
from anony.helpers._inline import recommendation_markup, stream_markup
from anony.helpers._queue import Queues
from anony.helpers._play import get_stream_url
from anony.utils.database import is_autoplay

class CallManager:
    def __init__(self):
        self.call = PyTgCalls(userbot.one) if userbot.one else None
        self.active_tracks = {}
        self.loops = {}

    async def start(self):
        if self.call:
            await self.call.start()
            print("[Music Flow] PyTgCalls audio client connected.")

    async def play(self, chat_id: int, track: dict):
        if not track.get("stream_url"):
            track["stream_url"] = await get_stream_url(track["link"])
        self.active_tracks[chat_id] = track
        stream = AudioPiped(track["stream_url"])
        if not self.call:
            return
        try:
            await self.call.join_group_call(chat_id, stream)
        except Exception:
            try:
                await self.call.change_stream(chat_id, stream)
            except Exception:
                pass

    async def on_song_end(self, chat_id: int):
        loop_count = self.loops.get(chat_id, 0)
        current = self.active_tracks.get(chat_id)
        if loop_count > 0 and current:
            self.loops[chat_id] -= 1
            await self.play(chat_id, current)
            return

        queue = Queues.get_queue(chat_id)
        if queue:
            next_track = Queues.pop_queue(chat_id)
            if not next_track.get("stream_url"):
                next_track["stream_url"] = await get_stream_url(next_track["link"])
            await self.play(chat_id, next_track)
            await app.send_message(
                chat_id=chat_id,
                text=f"🎵 **Now Playing:** [{next_track['title']}]({next_track['link']})",
                reply_markup=stream_markup(chat_id)
            )
            return

        last_track = self.active_tracks.get(chat_id)
        last_vid = last_track.get("id") if last_track else None
        if not last_vid:
            return

        autoplay_on = await is_autoplay(chat_id)
        recs = await YouTube.get_recommendations(last_vid, limit=9)

        if autoplay_on and recs:
            next_track = recs[0]
            next_track["stream_url"] = await get_stream_url(next_track["link"])
            await self.play(chat_id, next_track)
            await app.send_message(
                chat_id=chat_id,
                text=f"🎵 **AutoPlaying Next:** [{next_track['title']}]({next_track['link']})",
                reply_markup=stream_markup(chat_id)
            )
        elif recs:
            markup = recommendation_markup(recs, last_vid, offset=0)
            await app.send_message(
                chat_id=chat_id,
                text=(
                    "🎵 **Song Ended**\n\n"
                    "Choose a recommended track below, or turn on `/autoplay` for continuous stream:"
                ),
                reply_markup=markup
            )

MusicCall = CallManager()
