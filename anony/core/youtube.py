import asyncio
import yt_dlp
from youtubesearchpython import VideosSearch, Video

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="

    async def search(self, query: str):
        """Fast search using youtubesearchpython"""
        try:
            search = VideosSearch(query, limit=1)
            result = await asyncio.to_thread(search.result)
            if not result or not result.get("result"):
                return None
            track = result["result"][0]
            return {
                "title": track.get("title"),
                "id": track.get("id"),
                "link": track.get("link"),
                "duration": track.get("duration", "3:00"),
                "thumb": track.get("thumbnails", [{}])[0].get("url")
            }
        except Exception:
            return None

    async def get_recommendations(self, video_id: str, limit: int = 9):
        """Extract related videos directly from YouTube for AutoPlay"""
        try:
            url = f"{self.base}{video_id}"
            video_info = await asyncio.to_thread(Video.getInfo, url)
            if not video_info or "relatedVideos" not in video_info:
                return []
            
            recs = []
            for item in video_info["relatedVideos"].get("videos", []):
                recs.append({
                    "title": item.get("title"),
                    "id": item.get("id"),
                    "link": f"{self.base}{item.get('id')}",
                    "duration": item.get("duration", "3:00"),
                    "thumb": item.get("thumbnails", [{}])[0].get("url")
                })
                if len(recs) >= limit:
                    break
            return recs
        except Exception:
            return []

    async def get_playlist(self, url: str, limit: int = 50):
        """
        Fetches full YouTube playlists, Mixes (list=RD...), My Mix (list=RDMM...), 
        and user collections. Returns (playlist_title, list_of_tracks).
        """
        loop = asyncio.get_event_loop()
        def _extract():
            ydl_opts = {
                "extract_flat": "in_playlist",
                "skip_download": True,
                "quiet": True,
                "no_warnings": True,
                "ignoreerrors": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return None, []
                title = info.get("title") or "YouTube Playlist / Mix"
                raw_entries = info.get("entries") or []
                tracks = []
                for entry in raw_entries:
                    if not entry:
                        continue
                    vid_id = entry.get("id") or entry.get("url")
                    vid_title = entry.get("title")
                    if not vid_id or not vid_title:
                        continue
                    duration_sec = entry.get("duration")
                    if duration_sec:
                        m, s = divmod(int(duration_sec), 60)
                        h, m = divmod(m, 60)
                        dur_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
                    else:
                        dur_str = "3:00"
                    
                    track_link = f"{self.base}{vid_id}" if not vid_id.startswith("http") else vid_id
                    thumb_url = entry.get("thumbnails", [{}])[-1].get("url") if entry.get("thumbnails") else None

                    tracks.append({
                        "title": vid_title,
                        "id": vid_id,
                        "link": track_link,
                        "duration": dur_str,
                        "thumb": thumb_url
                    })
                    if len(tracks) >= limit:
                        break
                return title, tracks

        try:
            return await loop.run_in_executor(None, _extract)
        except Exception:
            return None, []

YouTube = YouTubeAPI()
