from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['project_roy']

def get_user_collection():
    return db['users']

def get_post_collection():
    return db['posts']

def get_story_collection():
    return db['stories']

def get_schedule_collection():
    return db['schedules']