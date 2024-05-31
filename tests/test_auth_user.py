def test_register_user(test_client, test_db, access_token):
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password": "newpassword2",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser2"
    assert data["email"] == "newuser2@example.com"


def test_login_user(test_client, test_db, mock_user_data):
    response = test_client.post(
        "/api/v1/auth/token",
        data={
            "username": mock_user_data[0]["username"],
            "password": "testpassword1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
