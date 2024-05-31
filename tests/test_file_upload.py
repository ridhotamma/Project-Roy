from fastapi.testclient import TestClient
from app.main import app
from fastapi import status
from app.config import AWS_CLOUDFRONT_DOMAIN_NAME

client = TestClient(app)


def test_upload_file_success(access_token):
    file_content = b"Test file content"
    files = {"file": ("test_file.txt", file_content, "text/plain")}

    response = client.post(
        "/api/v1/upload",
        files=files,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "file_url": f"{AWS_CLOUDFRONT_DOMAIN_NAME}/test_file.txt"
    }


def test_upload_file_failure():
    file_content = b"Test file content"
    files = {"file": ("test_file.txt", file_content, "text/plain")}

    response = client.post(
        "/api/v1/upload",
        files=files,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "message": "Authorization header missing",
        "status_code": 403,
    }
