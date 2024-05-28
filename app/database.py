from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['user_database']

def get_user_collection():
    return db['users']

def get_post_collection():
    return db['posts']

def get_story_collection():
    return db['stories']
