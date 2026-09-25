# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow

import asyncio
from pyrogram import enums, filters, types

from musicflow import app, config, db, lang
from musicflow.helpers import buttons, utils


@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    await m.reply_text(
        text=m.lang["help_menu"],
        reply_markup=buttons.help_markup(m.lang),
        quote=True,
    )


@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    if message.from_user.id in app.bl_users and message.from_user.id not in db.notified:
        return await message.reply_text(message.lang["bl_user_notify"])

    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    private = message.chat.type == enums.ChatType.PRIVATE
    _text = (
        message.lang["start_pm"].format(message.from_user.first_name, app.name)
        if private
        else message.lang["start_gp"].format(app.name)
    )

    key = buttons.start_key(message.lang, private)
    start_img = await db.get_asset("start") or config.START_IMG
    if not start_img or (not private and not await db.get_start_thumbnail(message.chat.id)):
        return await message.reply_text(_text, reply_markup=key, quote=not private)
    await message.reply_photo(
        photo=start_img,
        caption=_text,
        reply_markup=key,
        quote=not private,
    )

    if private:
        if await db.is_user(message.from_user.id):
            return
        await utils.send_log(message)
        await db.add_user(message.from_user.id)
    else:
        if await db.is_chat(message.chat.id):
            return
        await utils.send_log(message, True)
        await db.add_chat(message.chat.id)


@app.on_message(filters.command(["playmode", "settings"]) & filters.group & ~app.bl_users)
@lang.language()
async def settings(_, message: types.Message):
    admin_only = await db.get_play_mode(message.chat.id)
    cmd_delete = await db.get_cmd_delete(message.chat.id)
    _language = await db.get_lang(message.chat.id)
    await message.reply_text(
        text=message.lang["start_settings"].format(message.chat.title),
        reply_markup=buttons.settings_markup(
            message.lang, admin_only, cmd_delete, _language, message.chat.id
        ),
        quote=True,
    )


@app.on_message(filters.new_chat_members, group=7)
@lang.language()
async def _new_member(_, message: types.Message):
    if message.chat.type != enums.ChatType.SUPERGROUP:
        return await message.chat.leave()

    await asyncio.sleep(3)
    for member in message.new_chat_members:
        if member.id == app.id:
            if await db.is_chat(message.chat.id):
                return
            await utils.send_log(message, True)
            await db.add_chat(message.chat.id)

@app.on_message(filters.command(["autoplay", "thumbnail", "startthumbnail"]) & filters.group & ~app.bl_users)
@lang.language()
async def feature_settings(_, message: types.Message):
    from musicflow.helpers import admin_check
    if message.from_user.id not in app.sudoers and message.from_user.id not in await db.get_admins(message.chat.id):
        return await message.reply_text(message.lang["user_no_perms"])
    if len(message.command) < 2 or message.command[1].lower() not in {"on", "off"}:
        status = await db.get_autoplay(message.chat.id) if message.command[0] == "autoplay" else (await db.get_thumbnail(message.chat.id) if message.command[0] == "thumbnail" else await db.get_start_thumbnail(message.chat.id))
        return await message.reply_text(f"{message.command[0].title()}: {'ON' if status else 'OFF'}\nUsage: /{message.command[0]} on|off")
    enabled = message.command[1].lower() == "on"
    if message.command[0] == "autoplay":
        await db.set_autoplay(message.chat.id, enabled)
    elif message.command[0] == "thumbnail":
        await db.set_thumbnail(message.chat.id, enabled)
    else:
        await db.set_start_thumbnail(message.chat.id, enabled)
    await message.reply_text(f"{message.command[0].title()}: {'ON' if enabled else 'OFF'}")
