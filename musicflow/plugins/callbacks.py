# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of MusicFlow


import re
import time

from pyrogram import errors, filters, types

from musicflow import anon, app, db, lang, queue, tg, yt
from musicflow.helpers import admin_check, buttons, can_manage_vc

_recommend_refresh = {}


@app.on_callback_query(filters.regex("cancel_dl") & ~app.bl_users)
@lang.language()
async def cancel_dl(_, query: types.CallbackQuery):
    await query.answer()
    await tg.cancel(query)


@app.on_callback_query(filters.regex("controls") & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _controls(_, query: types.CallbackQuery):
    args = query.data.split()
    action, chat_id = args[1], int(args[2])
    qaction = len(args) == 4
    user = query.from_user.mention

    if not await db.get_call(chat_id):
        try:
            return await query.answer(query.lang["not_playing"], show_alert=True)
        except errors.QueryIdInvalid:
            try:
                await query.message.delete()
            except Exception:
                pass
            return

    if action == "status":
        return await query.answer()

    try:
        await query.answer(query.lang["processing"], show_alert=True)
    except errors.QueryIdInvalid:
        try:
            await query.message.delete()
        except Exception:
            pass
        return

    if action == "pause":
        if not await db.playing(chat_id):
            return await query.answer(
                query.lang["play_already_paused"], show_alert=True
            )
        await anon.pause(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["paused"], False)
            )
        status = query.lang["paused"]
        reply = query.lang["play_paused"].format(user)

    elif action == "resume":
        if await db.playing(chat_id):
            return await query.answer(query.lang["play_not_paused"], show_alert=True)
        await anon.resume(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["playing"], True)
            )
        reply = query.lang["play_resumed"].format(user)

    elif action == "skip":
        await anon.play_next(chat_id)
        status = query.lang["skipped"]
        reply = query.lang["play_skipped"].format(user)

    elif action == "force":
        pos, media = queue.check_item(chat_id, args[3])
        if not media or pos == -1:
            return await query.edit_message_text(query.lang["play_expired"])

        m_id = queue.get_current(chat_id).message_id
        queue.force_add(chat_id, media, remove=pos)
        try:
            await app.delete_messages(
                chat_id=chat_id, message_ids=[m_id, media.message_id], revoke=True
            )
            media.message_id = None
        except Exception:
            pass

        msg = await app.send_message(chat_id=chat_id, text=query.lang["play_next"])
        if not media.file_path:
            media.file_path = await yt.download(media.id, video=media.video)
        media.message_id = msg.id
        return await anon.play_media(chat_id, msg, media)

    elif action == "replay":
        media = queue.get_current(chat_id)
        media.user = user
        await anon.replay(chat_id)
        status = query.lang["replayed"]
        reply = query.lang["play_replayed"].format(user)

    elif action == "stop":
        await anon.stop(chat_id)
        status = query.lang["stopped"]
        reply = query.lang["play_stopped"].format(user)

    try:
        if action in ["skip", "replay", "stop"]:
            await query.message.reply_text(reply, quote=False)
            await query.message.delete()
        else:
            mtext = re.sub(
                r"\n\n<blockquote>.*?</blockquote>",
                "",
                query.message.caption.html or query.message.text.html,
                flags=re.DOTALL,
            )
            keyboard = buttons.controls(
                chat_id, status=status if action != "resume" else None
            )
        await query.edit_message_text(
            f"{mtext}\n\n<blockquote>{reply}</blockquote>", reply_markup=keyboard
        )
    except Exception:
        pass


@app.on_callback_query(filters.regex("help") & ~app.bl_users)
@lang.language()
async def _help(_, query: types.CallbackQuery):
    data = query.data.split()
    if len(data) == 1:
        return await query.answer(url=f"https://t.me/{app.username}?start=help")

    if data[1] == "back":
        return await query.edit_message_text(
            text=query.lang["help_menu"], reply_markup=buttons.help_markup(query.lang)
        )
    elif data[1] == "close":
        try:
            await query.message.delete()
            return await query.message.reply_to_message.delete()
        except Exception:
            return

    if data[1] == "settings":
        text = query.lang.get("help_settings", "<b>Group settings</b>\n\n/settings — Open the group playback settings.")
    elif data[1] == "autoplay":
        text = (
            "<b>Autoplay</b>\n\n"
            "When enabled, MusicFlow finds related tracks when the queue ends and continues playback automatically.\n\n"
            "Use <code>/autoplay on</code> or <code>/autoplay off</code> in a group.\n"
            "Group admins can change this setting."
        )
    else:
        text = query.lang[f"help_{data[1]}"]
    await query.edit_message_text(text=text, reply_markup=buttons.help_markup(query.lang, True))


@app.on_callback_query(filters.regex("settings") & ~app.bl_users)
@lang.language()
@admin_check
async def _settings_cb(_, query: types.CallbackQuery):
    cmd = query.data.split()
    if len(cmd) == 1:
        return await query.answer()
    await query.answer(query.lang["processing"], show_alert=True)

    chat_id = query.message.chat.id
    _admin = await db.get_play_mode(chat_id)
    _delete = await db.get_cmd_delete(chat_id)
    _language = await db.get_lang(chat_id)
    _autoplay = await db.get_autoplay(chat_id)
    _thumbnail = await db.get_thumbnail(chat_id)

    if cmd[1] == "autoplay":
        _autoplay = not _autoplay
        await db.set_autoplay(chat_id, _autoplay)
    elif cmd[1] == "thumbnail":
        _thumbnail = not _thumbnail
        await db.set_thumbnail(chat_id, _thumbnail)
    elif cmd[1] == "delete":
        _delete = not _delete
        await db.set_cmd_delete(chat_id, _delete)
    elif cmd[1] == "play":
        await db.set_play_mode(chat_id, _admin)
        _admin = not _admin
    await query.edit_message_reply_markup(
        reply_markup=buttons.settings_markup(
            query.lang,
            _admin,
            _delete,
            _language,
            chat_id,
            _autoplay,
            _thumbnail,
        )
    )

@app.on_callback_query(filters.regex(r"^recommend(?:_more)? ") & ~app.bl_users)
@lang.language()
async def recommendations(_, query: types.CallbackQuery):
    parts = query.data.split()
    chat_id = int(parts[1])
    if chat_id != query.message.chat.id:
        return await query.answer("This recommendation belongs to another chat.", show_alert=True)

    seed, ids = await db.get_recommendations(chat_id)
    recent = set(await db.get_recent(chat_id))
    if parts[0] == "recommend_more":
        if not seed:
            return await query.answer("There are no recommendations to refresh yet.", show_alert=True)
        now = time.monotonic()
        if now - _recommend_refresh.get(chat_id, 0) < 2.0:
            return await query.answer("Please wait a moment before refreshing again.", show_alert=True)
        _recommend_refresh[chat_id] = now
        recent.update(ids)
        current = queue.get_current(chat_id)
        if current:
            recent.add(current.id)
        tracks = await yt.recommend(seed, 4, recent)
        if not tracks:
            return await query.answer("No new recommendations are available right now.", show_alert=True)
        await db.set_recommendations(chat_id, seed, [x.id for x in tracks])
        await query.answer("Recommendations refreshed")
        return await query.edit_message_reply_markup(reply_markup=buttons.recommendations(chat_id, tracks))

    video_id = parts[2]
    if video_id not in ids:
        return await query.answer("This recommendation has expired. Please refresh the list.", show_alert=True)
    # Consume the selected recommendation immediately so repeated taps cannot queue it twice.
    remaining_ids = [item for item in ids if item != video_id]
    await db.set_recommendations(chat_id, seed, remaining_ids)
    await query.answer("Adding to queue…")
    track = await yt.search(video_id, query.message.id)
    if not track:
        return await query.answer("This track is no longer available.", show_alert=True)
    track.user = query.from_user.mention
    queue.add(chat_id, track)
    if not await db.get_call(chat_id):
        msg = await app.send_message(chat_id, "<b>Preparing your selection</b>\nGetting the audio ready…")
        track.file_path = await yt.download(track.id, video=track.video)
        if not track.file_path:
            return await msg.edit_text("<b>Could not prepare this track.</b>\nPlease choose another recommendation.")
        track.message_id = msg.id
        await anon.play_media(chat_id, msg, track)
    else:
        await query.message.edit_text("<b>Added to the queue</b>\nYour selection will play after the current queue.", reply_markup=buttons.play_queued(chat_id, track.id, "Play now"))
        # Prepare the next selected track in the background without blocking the callback.
        if not track.file_path:
            import asyncio
            asyncio.create_task(_prepare_recommendation(track))

async def _prepare_recommendation(track):
    try:
        if not track.file_path:
            track.file_path = await yt.download(track.id, video=track.video)
    except Exception:
        pass
