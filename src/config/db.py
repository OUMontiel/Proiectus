from pymongo import MongoClient
from dotenv import load_dotenv
import os
import motor

load_dotenv('.env')

conn = MongoClient(os.environ['MONGODB_URI'])
db = conn[os.environ['MONGODB_DBNAME']]
client = motor.motor_asyncio.AsyncIOMotorClient(
    os.environ['MONGODB_URI']
)
beanie_db = client[os.environ['MONGODB_DBNAME']]

