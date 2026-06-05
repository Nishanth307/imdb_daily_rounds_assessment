import os 
from dotenv import load_dotenv

load_dotenv() 

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    BATCH_SIZE = int(os.getenv("UPLOAD_BATCH_SIZE"))