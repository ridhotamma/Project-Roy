import pytest
import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.main import app
from app.auth.utils import hash_password


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_db():
    os.environ["MONGO_URL"] = "mongodb://localhost:27017/test_db"
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client["test_db"]
    yield db
    client.drop_database("test_db")


@pytest.fixture(scope="module")
def mock_user_data(test_db):
    users = [
        {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": hash_password("testpassword1"),
        },
        {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": hash_password("testpassword2"),
        },
    ]
    test_db["auth_users"].insert_many(users)
    return users


@pytest.fixture(scope="module")
def access_token(test_client, mock_user_data):
    response = test_client.post(
        "/api/v1/auth/token",
        data={
            "username": mock_user_data[0]["username"],
            "password": "testpassword1",
        },
    )
    data = response.json()
    return data["access_token"]


def pytest_unconfigure(config):
    os.environ.pop("MONGO_URL", None)
