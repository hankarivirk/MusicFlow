from motor.motor_asyncio import AsyncIOMotorClient
import config

if config.MONGO_DB_URI:
    try:
        _mongo = AsyncIOMotorClient(config.MONGO_DB_URI)
        mongodb = _mongo.MusicFlow
        print("[Music Flow] Connected to MongoDB database.")
    except Exception as e:
        print(f"[Music Flow] MongoDB connection failed: {e}")
        mongodb = None
else:
    mongodb = None
