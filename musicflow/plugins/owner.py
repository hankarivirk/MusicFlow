from pyrogram import filters, types

from musicflow import app, config, db


def _owner():
    return filters.user(config.OWNER_ID)


async def _photo_id(message: types.Message):
    photo = message.reply_to_message if message.reply_to_message and message.reply_to_message.photo else None
    if photo:
        return photo.photo.file_id
    return None


@app.on_message(filters.command("setstartimg") & _owner())
async def set_start_img(_, m: types.Message):
    file_id = await _photo_id(m)
    if not file_id:
        return await m.reply_text("<b>Start artwork</b>\nReply to a photo with <code>/setstartimg</code> to replace the current image.")
    await db.set_asset("start", file_id)
    await m.reply_text("<b>Start artwork updated</b>\nThe new image will be used for the configured start screen.")


@app.on_message(filters.command("setthumbimg") & _owner())
async def set_thumb_img(_, m: types.Message):
    file_id = await _photo_id(m)
    if not file_id:
        return await m.reply_text("<b>Now Playing artwork</b>\nReply to a photo with <code>/setthumbimg</code> to set the default fallback artwork.")
    await db.set_asset("thumb", file_id)
    await m.reply_text("<b>Default artwork updated</b>\nMusicFlow will use it whenever generated artwork is unavailable.")


@app.on_message(filters.command("setpingimg") & _owner())
async def set_ping_img(_, m: types.Message):
    file_id = await _photo_id(m)
    if not file_id:
        return await m.reply_text("<b>Ping artwork</b>\nReply to a photo with <code>/setpingimg</code> to replace the current image.")
    await db.set_asset("ping", file_id)
    await m.reply_text("<b>Ping artwork updated</b>\nThe new image is now active.")


@app.on_message(filters.command("resetstartimg") & _owner())
async def reset_start_img(_, m: types.Message):
    await db.set_asset("start", None)
    await m.reply_text("<b>Start artwork reset</b>\nThe configured fallback image is active again.")


@app.on_message(filters.command("resetthumbimg") & _owner())
async def reset_thumb_img(_, m: types.Message):
    await db.set_asset("thumb", None)
    await m.reply_text("<b>Default artwork reset</b>\nGenerated artwork will use the configured fallback when needed.")


@app.on_message(filters.command("resetpingimg") & _owner())
async def reset_ping_img(_, m: types.Message):
    await db.set_asset("ping", None)
    await m.reply_text("<b>Ping artwork reset</b>\nThe configured fallback image is active again.")


@app.on_message(filters.command("ownerhelp") & _owner())
async def owner_help(_, m: types.Message):
    await m.reply_text(
        "<b>Owner Controls</b>\n\n"
        "Manage MusicFlow's artwork and global playback behaviour from here.\n\n"
        "<b>Artwork</b>\n"
        "/setstartimg — set the start artwork\n"
        "/setthumbimg — set the Now Playing fallback\n"
        "/setpingimg — set the ping artwork\n"
        "/resetstartimg — restore the start fallback\n"
        "/resetthumbimg — restore the artwork fallback\n"
        "/resetpingimg — restore the ping fallback\n\n"
        "<b>Global playback</b>\n"
        "/globalthumb on|off\n"
        "/globalstartthumb on|off\n"
        "/globalautoplay on|off"
    )


async def _toggle(m: types.Message, setter, label: str):
    if len(m.command) < 2 or m.command[1].lower() not in {"on", "off"}:
        return await m.reply_text(f"<b>Usage</b>\n<code>/{m.command[0]} on|off</code>")
    enabled = m.command[1].lower() == "on"
    await setter(enabled)
    await m.reply_text(f"<b>{label}</b>\nStatus: {'On' if enabled else 'Off'}")


@app.on_message(filters.command("globalthumb") & _owner())
async def global_thumb(_, m):
    await _toggle(m, db.set_global_thumbnail, "Global YouTube thumbnail")


@app.on_message(filters.command("globalstartthumb") & _owner())
async def global_start_thumb(_, m):
    await _toggle(m, db.set_global_start_thumbnail, "Global start thumbnail")


@app.on_message(filters.command("globalautoplay") & _owner())
async def global_autoplay(_, m):
    await _toggle(m, db.set_global_autoplay, "Global autoplay")
