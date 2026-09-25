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
        return await m.reply_text("Reply to a photo with /setstartimg.")
    await db.set_asset("start", file_id)
    await m.reply_text("Start image updated.")


@app.on_message(filters.command("setthumbimg") & _owner())
async def set_thumb_img(_, m: types.Message):
    file_id = await _photo_id(m)
    if not file_id:
        return await m.reply_text("Reply to a photo with /setthumbimg.")
    await db.set_asset("thumb", file_id)
    await m.reply_text("Default thumbnail updated.")


@app.on_message(filters.command("setpingimg") & _owner())
async def set_ping_img(_, m: types.Message):
    file_id = await _photo_id(m)
    if not file_id:
        return await m.reply_text("Reply to a photo with /setpingimg.")
    await db.set_asset("ping", file_id)
    await m.reply_text("Ping image updated.")


@app.on_message(filters.command("resetstartimg") & _owner())
async def reset_start_img(_, m: types.Message):
    await db.set_asset("start", None)
    await m.reply_text("Start image reset to configured fallback.")


@app.on_message(filters.command("resetthumbimg") & _owner())
async def reset_thumb_img(_, m: types.Message):
    await db.set_asset("thumb", None)
    await m.reply_text("Default thumbnail reset to configured fallback.")


@app.on_message(filters.command("resetpingimg") & _owner())
async def reset_ping_img(_, m: types.Message):
    await db.set_asset("ping", None)
    await m.reply_text("Ping image reset to configured fallback.")


@app.on_message(filters.command("ownerhelp") & _owner())
async def owner_help(_, m: types.Message):
    await m.reply_text(
        "<b>MusicFlow Owner Panel</b>\n\n"
        "<b>Images</b>\n"
        "/setstartimg — reply to a photo\n"
        "/setthumbimg — reply to a photo\n"
        "/setpingimg — reply to a photo\n"
        "/resetstartimg\n/resetthumbimg\n/resetpingimg\n\n"
        "<b>Global controls</b>\n"
        "/globalthumb on|off\n"
        "/globalstartthumb on|off\n"
        "/globalautoplay on|off"
    )


async def _toggle(m: types.Message, setter, label: str):
    if len(m.command) < 2 or m.command[1].lower() not in {"on", "off"}:
        return await m.reply_text(f"Usage: {m.command[0]} on|off")
    enabled = m.command[1].lower() == "on"
    await setter(enabled)
    await m.reply_text(f"{label}: {'ON' if enabled else 'OFF'}")


@app.on_message(filters.command("globalthumb") & _owner())
async def global_thumb(_, m):
    await _toggle(m, db.set_global_thumbnail, "Global YouTube thumbnail")


@app.on_message(filters.command("globalstartthumb") & _owner())
async def global_start_thumb(_, m):
    await _toggle(m, db.set_global_start_thumbnail, "Global start thumbnail")


@app.on_message(filters.command("globalautoplay") & _owner())
async def global_autoplay(_, m):
    await _toggle(m, db.set_global_autoplay, "Global autoplay")
