from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

def start_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Add Music Flow to Group",
                url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Official Channel",
                url=config.SUPPORT_CHANNEL,
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def stream_markup(chat_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"cb_pause_{chat_id}"),
            InlineKeyboardButton(text="▶️ Resume", callback_data=f"cb_resume_{chat_id}"),
            InlineKeyboardButton(text="⏭ Skip", callback_data=f"cb_skip_{chat_id}"),
            InlineKeyboardButton(text="⏹ Stop", callback_data=f"cb_stop_{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="📢 Channel", url=config.SUPPORT_CHANNEL)
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def recommendation_markup(recs: list, base_vid: str, offset: int = 0):
    buttons = []
    current_recs = recs[offset : offset + 3]
    for r in current_recs:
        title = r["title"][:28] + "..." if len(r["title"]) > 28 else r["title"]
        buttons.append([
            InlineKeyboardButton(
                text=f"🎵 {title}",
                callback_data=f"rec_play_{r['id']}"
            )
        ])
    next_offset = offset + 3 if (offset + 3) < len(recs) else 0
    buttons.append([
        InlineKeyboardButton(
            text="✨ More Songs",
            callback_data=f"rec_more_{base_vid}_{next_offset}"
        )
    ])
    return InlineKeyboardMarkup(buttons)
