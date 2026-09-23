import asyncio
import time
import yt_dlp

# Cache stream URLs for 2 hours to provide instant 0ms replay
_stream_cache = {}
CACHE_TTL = 7200

async def get_stream_url(link: str) -> str:
    now = time.time()
    if link in _stream_cache:
        ts, url = _stream_cache[link]
        if now - ts < CACHE_TTL:
            return url

    loop = asyncio.get_event_loop()
    def _extract():
        opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "source_address": "0.0.0.0",
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get("url")
    
    url = await loop.run_in_executor(None, _extract)
    if url:
        _stream_cache[link] = (now, url)
    return url
