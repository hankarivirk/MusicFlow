# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow


import pyrogram

from musicflow import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="musicflow",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(self.logger, "Bot Started")
            get = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(f"Bot has failed to access the log group: {self.logger}\nReason: {ex}")

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Please promote the bot as an admin in logger group.")
        from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeChat
        common = [
            BotCommand("start", "Open MusicFlow"),
            BotCommand("help", "View available commands"),
            BotCommand("ping", "Check bot status"),
        ]
        group = [
            BotCommand("play", "Search and play a track"),
            BotCommand("vplay", "Play the video version"),
            BotCommand("queue", "View the upcoming queue"),
            BotCommand("playing", "View the current track"),
            BotCommand("pause", "Pause playback"),
            BotCommand("resume", "Resume playback"),
            BotCommand("skip", "Skip to the next track"),
            BotCommand("stop", "End the session"),
            BotCommand("settings", "Configure group preferences"),
            BotCommand("language", "Change the group language"),
        ]
        group_extra = [
            BotCommand("autoplay", "Toggle autoplay"),
            BotCommand("thumbnail", "Toggle song artwork"),
            BotCommand("auth", "Authorize a user"),
            BotCommand("unauth", "Remove authorization"),
            BotCommand("authlist", "View authorized users"),
            BotCommand("seek", "Seek within the track"),
            BotCommand("seekback", "Seek backward"),
            BotCommand("loop", "Set track looping"),
            BotCommand("end", "Stop playback"),
            BotCommand("next", "Skip the current track"),
            BotCommand("stats", "View bot statistics"),
        ]
        owner = [
            *common,
            *group,
            *group_extra,
            BotCommand("ownerhelp", "View owner controls"),
            BotCommand("setthumbimg", "Set the default artwork"),
            BotCommand("setstartimg", "Set the start artwork"),
            BotCommand("setpingimg", "Set the ping artwork"),
            BotCommand("globalthumb", "Toggle generated thumbnails"),
            BotCommand("globalstartthumb", "Toggle start artwork"),
            BotCommand("globalautoplay", "Toggle global autoplay"),
            BotCommand("resetstartimg", "Restore the start artwork"),
            BotCommand("resetthumbimg", "Restore the artwork fallback"),
            BotCommand("resetpingimg", "Restore the ping artwork"),
        ]
        await self.set_bot_commands(common, scope=BotCommandScopeAllPrivateChats())
        await self.set_bot_commands(group, scope=BotCommandScopeAllGroupChats())
        await self.set_bot_commands(owner, scope=BotCommandScopeChat(chat_id=self.owner))
        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
