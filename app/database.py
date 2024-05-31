import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/project_roy")
    client = MongoClient(mongo_url)
    db = client.get_database()
    return db


def get_ig_user_collection():
    return get_database()["users"]


def get_auth_user_collection():
    return get_database()["auth_users"]


def get_post_collection():
    return get_database()["posts"]


def get_story_collection():
    return get_database()["stories"]


def get_schedule_collection():
    return get_database()["schedules"]


def get_gallery_collection():
    return get_database()["galleries"]
