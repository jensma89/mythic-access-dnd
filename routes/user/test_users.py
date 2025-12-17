# """
# test_users.py
# 
# Test the user endpoints.
# """
# from fastapi.testclient import TestClient
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token
# 
# 
# 
# # Override DB with test DB
# app.dependency_overrides[prod_get_session] = get_test_session
# 
# 
# def auth_header(user):
#     """Create a authentication header."""
#     token = get_test_token(user)
#     return {"Authorization": f"Bearer {token}"}
# 
# 
# 
# def test_get_single_user():
#     """Test to retrieve a single user by ID."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         f"/users/{user.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["id"] == user.id
#     assert data["user_name"] == user.user_name
# 
# 
# def test_get_single_user_not_found():
#     """Test for user not found."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         "/users/99999",
#         headers=auth_header(create_test_user(
#             next(get_test_session())
#         )
#         )
#     )
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]
# 
# 
# def test_get_single_user_unauthorized():
#     """Test to get a single user
#     from unauthorized user."""
#     client = TestClient(app)
#     response = client.get("/users/1")
#     assert response.status_code == 401
# 
# 
# 
# def test_list_users():
#     """Test list users."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user_1 = create_test_user(session)
#     user_2 = create_test_user(session)
#     response = client.get(
#         "/users/",
#         headers=auth_header(user_1)
#     )
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) >= 2
# 
# 
# def test_list_users_unauthorized():
#     """Test list users by unauthorized user."""
#     client = TestClient(app)
#     response = client.get("/users/")
#     assert response.status_code == 401
# 
# 
# def test_update_user():
#     """Test for update a user."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.patch(
#         "/users/me/update",
#         json={"user_name": "updated_name"},
#         headers=auth_header(user)
#     )
# 
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user_name"] == "updated_name"
# 
# 
# def test_update_user_unauthorized():
#     """Test update a user by a unauthorized user."""
#     client = TestClient(app)
#     response = client.patch(
#         "/users/me/update",
#         json={"user_name": "x"}
#     )
#     assert response.status_code == 401
# 
# 
# 
# def test_delete_user():
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.delete(
#         "/users/me/delete",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
# 
#     # Now it should be gone
#     check = client.get(
#         f"/users/{user.id}",
#         headers=auth_header(user)
#     )
#     assert check.status_code in (401, 404)
# 
# 
# def test_delete_user_unauthorized():
#     """Test to delete a user by a unauthorized user."""
#     client = TestClient(app)
#     response = client.delete("/users/me/delete")
#     assert response.status_code == 401


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from fastapi import HTTPException, Request
from routes.user.users import read_user, read_users, update_user, delete_user
from models.schemas.user_schema import UserUpdate, UserPublic
from models.db_models.table_models import User
from services.user.user_service_exceptions import UserNotFoundError
from dependencies import UserQueryParams, Pagination
from datetime import datetime


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_service():
    """Fixture for mocked user service."""
    return Mock()


@pytest.fixture
def mock_user():
    """Fixture for mocked current user."""
    user = User(
        id=1,
        user_name="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        created_at=datetime.now()
    )
    return user


@pytest.fixture
def sample_user_public():
    """Fixture for sample user public."""
    return UserPublic(
        id=1,
        user_name="testuser",
        email="test@example.com",
        created_at=datetime.now()
    )


@pytest.fixture
def mock_pagination():
    """Fixture for mocked pagination."""
    return Pagination(offset=0, limit=100)


@pytest.fixture
def mock_filters():
    """Fixture for mocked user query params."""
    return UserQueryParams()


# Tests for read_user function
def test_read_user_success(mock_request, mock_service, mock_user, sample_user_public):
    """Test successful user retrieval."""
    mock_service.get_user.return_value = sample_user_public

    result = read_user(mock_request, 1, mock_user, mock_service)

    mock_service.get_user.assert_called_once_with(1)
    assert result.id == sample_user_public.id
    assert result.user_name == sample_user_public.user_name


def test_read_user_not_found(mock_request, mock_service, mock_user):
    """Test read user raises HTTPException when user not found."""
    mock_service.get_user.side_effect = UserNotFoundError("User not found")

    with pytest.raises(HTTPException) as exc_info:
        read_user(mock_request, 999, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found."


def test_read_user_exception(mock_request, mock_service, mock_user):
    """Test read user raises HTTPException on generic exception."""
    mock_service.get_user.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc_info:
        read_user(mock_request, 1, mock_user, mock_service)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal server error."


# Tests for read_users function
def test_read_users_success(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test successful users list retrieval."""
    users = [
        UserPublic(id=1, user_name="user1", email="user1@example.com", created_at=datetime.now()),
        UserPublic(id=2, user_name="user2", email="user2@example.com", created_at=datetime.now())
    ]
    mock_service.list_users.return_value = users

    result = read_users(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    mock_service.list_users.assert_called_once_with(
        offset=0,
        limit=100,
        filters=mock_filters
    )
    assert len(result) == 2
    assert result[0].user_name == "user1"
    assert result[1].user_name == "user2"


def test_read_users_empty(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test users list returns empty list."""
    mock_service.list_users.return_value = []

    result = read_users(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    assert isinstance(result, list)
    assert len(result) == 0


# Tests for update_user function
def test_update_user_success(mock_request, mock_service, mock_user, sample_user_public):
    """Test successful user update."""
    updated_user = UserPublic(
        id=1,
        user_name="updateduser",
        email="test@example.com",
        created_at=datetime.now()
    )
    mock_service.update_user.return_value = updated_user

    update_data = UserUpdate(user_name="updateduser")
    result = update_user(mock_request, update_data, mock_user, mock_service)

    mock_service.update_user.assert_called_once_with(1, update_data)
    assert result.user_name == "updateduser"


def test_update_user_not_found(mock_request, mock_service, mock_user):
    """Test update user raises HTTPException when update returns None."""
    mock_service.update_user.return_value = None

    update_data = UserUpdate(user_name="newname")

    with pytest.raises(HTTPException) as exc_info:
        update_user(mock_request, update_data, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


# Tests for delete_user function
def test_delete_user_success(mock_request, mock_service, mock_user, sample_user_public):
    """Test successful user deletion."""
    mock_service.delete_user.return_value = sample_user_public

    result = delete_user(mock_request, mock_user, mock_service)

    mock_service.delete_user.assert_called_once_with(1)
    assert result.id == sample_user_public.id


def test_delete_user_not_found(mock_request, mock_service, mock_user):
    """Test delete user raises HTTPException when delete returns None."""
    mock_service.delete_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        delete_user(mock_request, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
