import pytest
from fastapi.testclient import TestClient
from user_service import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "testpass123"
    }

def test_signup(test_user):
    response = client.post("/signup", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]

def test_login(test_user):
    response = client.post("/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_get_me(test_user):
    login_response = client.post("/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == test_user["email"]
