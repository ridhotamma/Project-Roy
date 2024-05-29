def test_register_user(test_client, test_db):
    response = test_client.post(
        "/auth/register",
        json={
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password": "newpassword2",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser2"
    assert data["email"] == "newuser2@example.com"


def test_login_user(test_client, test_db, mock_user_data):
    response = test_client.post(
        "/auth/token",
        data={
            "username": "testuser1",
            "password": "testpassword1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
