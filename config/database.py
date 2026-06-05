from pymongo import MongoClient
from config.setting import Config

try:
    client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
except Exception as e:
    raise ConnectionError(
        "Failed to connect to MongoDB start the mongo service and try again"
    ) from e

db = client[Config.DB_NAME]
