import aiohttp
import config

_telegraph_token = None

async def get_telegraph_token() -> str:
    global _telegraph_token
    if _telegraph_token:
        return _telegraph_token
    async with aiohttp.ClientSession() as session:
        url = "https://api.telegra.ph/createAccount"
        data = {"short_name": "MusicFlow", "author_name": config.BOT_NAME}
        try:
            async with session.post(url, data=data) as resp:
                res = await resp.json()
                if res.get("ok"):
                    _telegraph_token = res["result"]["access_token"]
                    return _telegraph_token
        except Exception:
            pass
    return None

async def create_telegraph_queue_page(title: str, tracks: list) -> str:
    """
    Publishes long queue or full playlist tracks to a clean Telegraph web page.
    Returns the public Telegraph URL.
    """
    token = await get_telegraph_token()
    if not token:
        return None

    # Construct Telegraph HTML/DOM structure
    content = [
        {"tag": "h3", "children": [f"{title} - Music Flow Queue"]},
        {"tag": "p", "children": [f"Total Tracks in Queue: {len(tracks)}"]},
        {"tag": "hr"},
    ]

    for i, t in enumerate(tracks, 1):
        line = f"{i}. {t.get('title')} ({t.get('duration', '3:00')}) - by {t.get('requester', 'Anonymous')}"
        content.append({"tag": "p", "children": [line]})

    async with aiohttp.ClientSession() as session:
        url = "https://api.telegra.ph/createPage"
        payload = {
            "access_token": token,
            "title": f"Queue ({len(tracks)} Songs) - {config.BOT_NAME}",
            "author_name": config.BOT_NAME,
            "author_url": config.SUPPORT_CHANNEL,
            "content": str(content).replace("'", '"'),
            "return_content": False,
        }
        try:
            async with session.post(url, json=payload) as resp:
                res = await resp.json()
                if res.get("ok"):
                    return res["result"]["url"]
        except Exception:
            pass
    return None
