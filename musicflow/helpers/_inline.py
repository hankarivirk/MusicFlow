# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow


from pyrogram import types

from musicflow import app, config, lang
from musicflow.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data=f"cancel_dl")]])

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append(
                [self.ikb(text=status, callback_data=f"controls status {chat_id}")]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=timer, callback_data=f"controls status {chat_id}")]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="▶", callback_data=f"controls resume {chat_id}"),
                    self.ikb(text="⏸", callback_data=f"controls pause {chat_id}"),
                    self.ikb(text="↻", callback_data=f"controls replay {chat_id}"),
                    self.ikb(text="⏭", callback_data=f"controls skip {chat_id}"),
                    self.ikb(text="⏹", callback_data=f"controls stop {chat_id}"),
                ]
            )
        return self.ikm(keyboard)

    def help_markup(self, _lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            return self.ikm([[
                self.ikb(text=_lang["back"], callback_data="help back"),
                self.ikb(text=_lang["close"], callback_data="help close"),
            ]])
        categories = [
            ("🎼 Music", "play"), ("🎚️ Playback", "admins"), ("🗂️ Queue", "queue"),
            ("🎛️ Settings", "settings"), ("📊 Stats", "stats"), ("🛰️ More", "ping"),
        ]
        rows = [[self.ikb(text=label, callback_data=f"help {key}") for label, key in categories[i:i+2]]
                for i in range(0, len(categories), 2)]
        rows.append([self.ikb(text="Close", callback_data="help close")])
        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, url=config.CHANNEL)]])

    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text, callback_data=f"controls force {chat_id} {item_id}"
                    )
                ]
            ]
        )

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q")]]
        )

    def settings_markup(
        self, lang: dict, admin_only: bool, cmd_delete: bool, language: str, chat_id: int,
        autoplay: bool = False, thumbnail: bool = True,
    ) -> types.InlineKeyboardMarkup:
        state = lambda value: "On" if value else "Off"
        return self.ikm([
            [self.ikb(text="🗝️ Admin-only playback", callback_data="settings"),
             self.ikb(text=state(admin_only), callback_data="settings play")],
            [self.ikb(text="🧹 Command cleanup", callback_data="settings"),
             self.ikb(text=state(cmd_delete), callback_data="settings delete")],
            [self.ikb(text="🪄 Autoplay", callback_data="settings"),
             self.ikb(text=state(autoplay), callback_data=f"settings autoplay {chat_id}")],
            [self.ikb(text="🖼️ Song artwork", callback_data="settings"),
             self.ikb(text=state(thumbnail), callback_data=f"settings thumbnail {chat_id}")],
            [self.ikb(text="🗺️ Language", callback_data="settings"),
             self.ikb(text=lang_codes[language], callback_data="language")],
        ])

    def start_key(
        self, lang: dict, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        rows = [
            [self.ikb(text=lang["add_me"], url=f"https://t.me/{app.username}?startgroup=true")],
            [self.ikb(text=lang["help"], callback_data="help")],
        ]
        links = []
        if config.UPDATES_CHANNEL:
            links.append(self.ikb(text="🛎️ Updates", url=config.UPDATES_CHANNEL))
        if config.CHANNEL:
            links.append(self.ikb(text="📯 Channel", url=config.CHANNEL))
        if links:
            rows.append(links)
        if not private:
            rows.append([self.ikb(text=lang["language"], callback_data="language")])
        return self.ikm(rows)

    def recommendations(self, chat_id: int, tracks: list) -> types.InlineKeyboardMarkup:
        rows = []
        for track in tracks[:4]:
            title = (track.title or "Recommended track").strip()
            rows.append([self.ikb(text=title[:38], callback_data=f"recommend {chat_id} {track.id}")])
        rows.append([self.ikb(text="🎲 Refresh recommendations", callback_data=f"recommend_more {chat_id}")])
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="📋", copy_text=link),
                    self.ikb(text="YouTube", url=link),
                ],
            ]
        )
