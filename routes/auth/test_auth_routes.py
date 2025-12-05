"""
test_auth_routes.py

Test the auth endpoints for register/login and users/me.
"""
from fastapi.testclient import TestClient

from main import app
from dependencies import get_session as prod_get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token



# Override the DB dependency for tests
app.dependency_overrides[prod_get_session] = get_test_session

client = TestClient(app)


# Success tests

def test_register():
    """Test user registration using the test DB."""
    session = next(get_test_session())

    response = client.post(
        "/auth/register",
        json={
            "user_name": "newtester",
            "email": "newtester@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["user_name"] == "newtester"
    assert "id" in data
    assert "created_at" in data


def test_login():
    """Test the user login using the test DB."""
    # Use test session
    session = next(get_test_session())
    test_user = create_test_user(session)

    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    json_resp = response.json()
    assert "access_token" in json_resp
    assert "token_type" in json_resp


def test_me():
    """Test the /auth/me endpoint."""
    session = next(get_test_session())
    test_user = create_test_user(session)

    token = get_test_token(test_user)

    response = client.get(
        "auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == test_user.id
    assert data["user_name"] == test_user.user_name
    assert data["email"] == test_user.email


# Error tests

def test_register_duplicate_email():
    """Registering the same email twice."""
    session = next(get_test_session())

    # First user (normal)
    client.post(
        "/auth/register",
        json={
            "user_name": "dup",
            "email": "dup@example.com",
            "password": "password123"
        }
    )


    # Second user → expect failure
    response = client.post(
        "/auth/register",
        json={
            "user_name": "dup2",
            "email": "dup@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400


def test_login_wrong_password():
    """Login with incorrect password."""
    session = next(get_test_session())
    test_user = create_test_user(session)

    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "WRONGPASS"
        }
    )

    assert response.status_code == 401


def test_login_user_not_found():
    """Login with non existen email."""
    response = client.post(
        "/auth/login",
        data={
            "username": "idontexist@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401


def test_me_unauthorized():
    """Calling /me without a token."""
    response = client.get("/auth/me")

    assert response.status_code == 401
