from anony.core.mongo import mongodb
import config

_memory_db = {
    "autoplay": {},
    "sudoers": set(config.SUDO_USERS),
    "auth": {},
    "blacklist_chats": set(),
    "loop": {},
    "language": {},
}

async def is_autoplay(chat_id: int) -> bool:
    if mongodb is not None:
        try:
            doc = await mongodb.autoplay.find_one({"chat_id": chat_id})
            return doc.get("status", False) if doc else False
        except Exception:
            pass
    return _memory_db["autoplay"].get(chat_id, False)

async def set_autoplay(chat_id: int, status: bool):
    _memory_db["autoplay"][chat_id] = status
    if mongodb is not None:
        try:
            await mongodb.autoplay.update_one(
                {"chat_id": chat_id},
                {"$set": {"status": status}},
                upsert=True
            )
        except Exception:
            pass

async def is_sudo(user_id: int) -> bool:
    if user_id in config.SUDO_USERS or user_id == config.OWNER_ID:
        return True
    if mongodb is not None:
        try:
            doc = await mongodb.sudoers.find_one({"user_id": user_id})
            return bool(doc)
        except Exception:
            pass
    return user_id in _memory_db["sudoers"]

async def add_sudo(user_id: int):
    _memory_db["sudoers"].add(user_id)
    if mongodb is not None:
        try:
            await mongodb.sudoers.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        except Exception:
            pass

async def remove_sudo(user_id: int):
    _memory_db["sudoers"].discard(user_id)
    if mongodb is not None:
        try:
            await mongodb.sudoers.delete_one({"user_id": user_id})
        except Exception:
            pass

async def is_blacklisted(chat_id: int) -> bool:
    if mongodb is not None:
        try:
            doc = await mongodb.blacklist.find_one({"chat_id": chat_id})
            return bool(doc)
        except Exception:
            pass
    return chat_id in _memory_db["blacklist_chats"]

async def blacklist_chat(chat_id: int):
    _memory_db["blacklist_chats"].add(chat_id)
    if mongodb is not None:
        try:
            await mongodb.blacklist.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)
        except Exception:
            pass

async def whitelist_chat(chat_id: int):
    _memory_db["blacklist_chats"].discard(chat_id)
    if mongodb is not None:
        try:
            await mongodb.blacklist.delete_one({"chat_id": chat_id})
        except Exception:
            pass

async def get_lang(chat_id: int) -> str:
    if mongodb is not None:
        try:
            doc = await mongodb.language.find_one({"chat_id": chat_id})
            if doc:
                return doc.get("lang", "en")
        except Exception:
            pass
    return _memory_db["language"].get(chat_id, "en")

async def set_lang(chat_id: int, lang: str):
    _memory_db["language"][chat_id] = lang
    if mongodb is not None:
        try:
            await mongodb.language.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)
        except Exception:
            pass


# Thumbnail settings
async def is_thumb_enabled(chat_id: int) -> bool:
    global_default = _memory_db.get("global_thumb", True)
    if mongodb is not None:
        try:
            doc = await mongodb.thumbnail.find_one({"chat_id": chat_id})
            if doc is not None:
                return doc.get("status", global_default)
            g_doc = await mongodb.settings.find_one({"setting": "global_thumb"})
            if g_doc is not None:
                return g_doc.get("status", True)
        except Exception:
            pass
    return _memory_db.get("thumbnails", {}).get(chat_id, global_default)

async def set_thumb(chat_id: int, status: bool):
    _memory_db.setdefault("thumbnails", {})[chat_id] = status
    if mongodb is not None:
        try:
            await mongodb.thumbnail.update_one(
                {"chat_id": chat_id},
                {"$set": {"status": status}},
                upsert=True
            )
        except Exception:
            pass

async def set_global_thumb(status: bool):
    _memory_db["global_thumb"] = status
    if mongodb is not None:
        try:
            await mongodb.settings.update_one(
                {"setting": "global_thumb"},
                {"$set": {"status": status}},
                upsert=True
            )
        except Exception:
            pass

# Cleanmode settings
async def is_cleanmode(chat_id: int) -> bool:
    if mongodb is not None:
        try:
            doc = await mongodb.cleanmode.find_one({"chat_id": chat_id})
            if doc is not None:
                return doc.get("status", True)
        except Exception:
            pass
    return _memory_db.get("cleanmode", {}).get(chat_id, True)

async def set_cleanmode(chat_id: int, status: bool):
    _memory_db.setdefault("cleanmode", {})[chat_id] = status
    if mongodb is not None:
        try:
            await mongodb.cleanmode.update_one(
                {"chat_id": chat_id},
                {"$set": {"status": status}},
                upsert=True
            )
        except Exception:
            pass
