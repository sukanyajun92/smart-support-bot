# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_service.main import app
from user_service.models import Base, UserDB
from user_service.dependencies import get_db
from user_service.auth import get_password_hash

# SQLite in-memory test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_user():
    return {"email": "test@example.com", "name": "Test User", "password": "testpass"}

def test_signup(test_user):
    response = client.post("/signup", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]

def test_login_and_me(test_user):
    # Signup first
    client.post("/signup", json=test_user)

    # Login
    response = client.post("/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Authenticated /me request
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    me = response.json()
    assert me["email"] == test_user["email"]
    assert me["name"] == test_user["name"]
