import time
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from anony.utils.database import is_sudo
import config

# In-memory admin cache to prevent Telegram FloodWait: {chat_id: (timestamp, {user_ids})}
_admin_cache = {}
CACHE_TTL = 900  # 15 minutes

async def get_chat_admins(chat) -> set:
    chat_id = chat.id
    now = time.time()
    if chat_id in _admin_cache:
        ts, admins = _admin_cache[chat_id]
        if now - ts < CACHE_TTL:
            return admins

    admins = set()
    try:
        async for member in chat.get_members(filter=None):
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                if member.user:
                    admins.add(member.user.id)
    except Exception:
        pass
    _admin_cache[chat_id] = (now, admins)
    return admins

async def is_admin(message: Message) -> bool:
    if not message.from_user:
        return False
    user_id = message.from_user.id
    if await is_sudo(user_id):
        return True
    
    admins = await get_chat_admins(message.chat)
    if user_id in admins:
        return True
    
    # Fallback to direct check if not found in cache
    try:
        member = await message.chat.get_member(user_id)
        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            admins.add(user_id)
            return True
    except Exception:
        pass
    return False
