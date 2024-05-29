# app/database.py

import os
from pymongo import MongoClient

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/project_roy")

client = MongoClient(mongo_url)
db = client.get_database()

def get_user_collection():
    return db['users']

def get_post_collection():
    return db['posts']

def get_story_collection():
    return db['stories']

def get_schedule_collection():
    return db['schedules']
