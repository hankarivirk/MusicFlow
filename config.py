from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Mandatory Telegram API Credentials
API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", "0"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "0"))
MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# Assistant String Sessions (Up to 5)
STRING_SESSION = getenv("STRING_SESSION", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")

# Branding & Community
BOT_NAME = getenv("BOT_NAME", "Music Flow")
BOT_USERNAME = getenv("BOT_USERNAME", "")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/YourChannel")

# Permissions
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split())) if getenv("SUDO_USERS") else []
if OWNER_ID and OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# Limits
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "300"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "50"))

# Pure URL Image Assets
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/8b0062b1b31a830b806f1.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/8b0062b1b31a830b806f1.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://telegra.ph/file/8b0062b1b31a830b806f1.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/8b0062b1b31a830b806f1.jpg")
