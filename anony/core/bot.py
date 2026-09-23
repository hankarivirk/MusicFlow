from pyrogram import Client
import config

class MusicBot(Client):
    def __init__(self):
        super().__init__(
            name="MusicFlowBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name
        config.BOT_USERNAME = get_me.username
        print(f"[Music Flow] Bot running as @{self.username} (ID: {self.id})")

    async def stop(self):
        await super().stop()
        print("[Music Flow] Bot stopped.")

Bot = MusicBot()
