import asyncio
import importlib
from pyrogram import idle
from anony.core.bot import Bot
from anony.core.userbot import userbot
from anony.core.calls import MusicCall
from anony.core.dir import check_dirs
from anony.core.lang import load_languages
from anony.plugins import ALL_PLUGINS
import config

async def init():
    check_dirs()
    load_languages()
    print("[Music Flow] Starting Bot & Assistant...")
    await Bot.start()
    await userbot.start()
    await MusicCall.start()

    for p in ALL_PLUGINS:
        try:
            importlib.import_module(f"anony.plugins.{p}")
        except Exception as e:
            print(f"[Music Flow] Error loading plugin '{p}': {e}")
    print(f"[Music Flow] Successfully loaded {len(ALL_PLUGINS)} plugins.")
    print("[Music Flow] Ready to stream.")

    await idle()
    await Bot.stop()
    await userbot.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
