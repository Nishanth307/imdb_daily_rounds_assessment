from pymongo import MongoClient
from config.setting import Config


client = MongoClient(Config.MONGO_URI)

db = client[Config.DB_NAME]
