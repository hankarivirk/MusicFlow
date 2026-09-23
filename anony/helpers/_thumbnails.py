import config

def get_thumbnail_url(track_thumb: str = None) -> str:
    if track_thumb and track_thumb.startswith("http"):
        return track_thumb
    return config.STREAM_IMG_URL
