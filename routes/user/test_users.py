"""
test_users.py

Test the user endpoints.
"""
from fastapi.testclient import TestClient

from main import app
from dependencies import get_session as prod_get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token



# Override DB with test DB
app.dependency_overrides[prod_get_session] = get_test_session


def auth_header(user):
    """Create a authentication header."""
    token = get_test_token(user)
    return {"Authorization": f"Bearer {token}"}



def test_get_single_user():
    """Test to retrieve a single user by ID."""
    client = TestClient(app)
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.get(
        f"/users/{user.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user.id
    assert data["user_name"] == user.user_name


def test_get_single_user_not_found():
    """Test for user not found."""
    client = TestClient(app)
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.get(
        "/users/99999",
        headers=auth_header(create_test_user(
            next(get_test_session())
        )
        )
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_single_user_unauthorized():
    """Test to get a single user
    from unauthorized user."""
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 401



def test_list_users():
    """Test list users."""
    client = TestClient(app)
    session = next(get_test_session())
    user_1 = create_test_user(session)
    user_2 = create_test_user(session)

    response = client.get(
        "/users/",
        headers=auth_header(user_1)
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_list_users_unauthorized():
    """Test list users by unauthorized user."""
    client = TestClient(app)
    response = client.get("/users/")
    assert response.status_code == 401


def test_update_user():
    """Test for update a user."""
    client = TestClient(app)
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.patch(
        "/users/me/update",
        json={"user_name": "updated_name"},
        headers=auth_header(user)
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "updated_name"


def test_update_user_unauthorized():
    """Test update a user by a unauthorized user."""
    client = TestClient(app)
    response = client.patch(
        "/users/me/update",
        json={"user_name": "x"}
    )
    assert response.status_code == 401



def test_delete_user():
    client = TestClient(app)
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.delete(
        "/users/me/delete",
        headers=auth_header(user)
    )
    assert response.status_code == 200

    # Now it should be gone
    check = client.get(
        f"/users/{user.id}",
        headers=auth_header(user)
    )
    assert check.status_code in (401, 404)


def test_delete_user_unauthorized():
    """Test to delete a user by a unauthorized user."""
    client = TestClient(app)
    response = client.delete("/users/me/delete")
    assert response.status_code == 401
