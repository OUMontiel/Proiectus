from pymongo import MongoClient
from dotenv import load_dotenv
import os 

load_dotenv('.env')

conn = MongoClient(os.environ['MONGODB_URI'])
db = conn[os.environ['MONGODB_DBNAME']]