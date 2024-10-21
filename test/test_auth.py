import pytest
from fastapi import status
from app.db.base import get_db
from app.db.models.users import Users
from app.main import app
from app.schemas.users import CreateUserRequest
from test.utils import override_get_db, client, test_user, TestingSessionLocal


app.dependency_overrides[get_db] = override_get_db


def test_login_for_access_token(test_user):

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "appu", "password": "testpassword"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_credentials(test_user):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "test", "password": "testpassword"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_user(test_user):
    user_data = {
        "username": "newuser",
        "email": "newuser@email.com",
        "first_name": "New",
        "last_name": "User",
        "password": "newpassword",
        "role": "admin",
        "phone_number": "(222)-222-2222",
    }

    response = client.post("/api/v1/auth/", json=user_data)
    response.status_code == 201
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 2).first()
    assert model.username == user_data.get("username")


def test_reset_password(test_user):
    response = client.post(
        "/api/v1/auth/password",
        json={"password": "testpassword", "new_password": "newpassord"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
