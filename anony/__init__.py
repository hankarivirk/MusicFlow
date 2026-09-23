import config
from pyrogram import Client

app = Client(
    name="MusicFlowBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)
