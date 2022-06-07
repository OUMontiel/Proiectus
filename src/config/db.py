from pymongo import MongoClient
from dotenv import load_dotenv
import os
import motor

if os.environ.get('ENV') == 'test':
    print('Running in test mode')
    load_dotenv('test.env')
else:
    print('Running in dev mode')
    load_dotenv('.env')

db_uri = os.environ['MONGODB_URI']
db_name = os.environ['MONGODB_DBNAME']


# TODO Eliminar, ya no usar pymonho
conn = MongoClient(db_uri)
db = conn[db_name]

client = motor.motor_asyncio.AsyncIOMotorClient(db_uri)
beanie_db = client[db_name]
