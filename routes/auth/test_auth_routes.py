# """
# test_auth_routes.py
# 
# Test the auth endpoints for register/login and users/me.
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
# # Override the DB dependency for tests
# app.dependency_overrides[prod_get_session] = get_test_session
# 
# 
# # Success tests
# 
# def test_register():
#     """Test user registration using the test DB."""
#     session = Session(test_engine)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/register",
#         json={
#             "user_name": "newtester",
#             "email": "newtester@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["user_name"] == "newtester"
#     assert "id" in data
#     assert "created_at" in data
# 
# 
# def test_login():
#     """Test the user login using the test DB."""
#     # Use test session
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": test_user.email,
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 200
# 
#     json_resp = response.json()
#     assert "access_token" in json_resp
#     assert "token_type" in json_resp
# 
# 
# def test_me():
#     """Test the /auth/me endpoint."""
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     token = get_test_token(test_user)
# 
#     auth_client = TestClient(app)
#     auth_client.headers = {"Authorization": f"Bearer {token}"}
# 
#     response = auth_client.get("/auth/me")
# 
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["id"] == test_user.id
#     assert data["user_name"] == test_user.user_name
#     assert data["email"] == test_user.email
# # Error tests
# 
# def test_register_duplicate_email():
#     """Registering the same email twice."""
#     session = Session(test_engine)
#     client = TestClient(app)
# 
#     # First user (normal)
#     client.post(
#         "/auth/register",
#         json={
#             "user_name": "dup",
#             "email": "dup@example.com",
#             "password": "password123"
#         }
#     )
# 
#     # Second user → expect failure
#     response = client.post(
#         "/auth/register",
#         json={
#             "user_name": "dup2",
#             "email": "dup@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 400
# 
# 
# def test_login_wrong_password():
#     """Login with incorrect password."""
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": test_user.email,
#             "password": "WRONGPASS"
#         }
#     )
# 
#     assert response.status_code == 401
# 
# 
# def test_login_user_not_found():
#     """Login with non existen email."""
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": "idontexist@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 401
# 
# 
# def test_me_unauthorized():
#     """Calling /me without a token."""
#     client = TestClient(app)
#
#     response = client.get("/auth/me")
#
#     assert response.status_code == 401


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from routes.auth.auth_routes import register_user, login_for_access_token, get_my_profile
from models.schemas.user_schema import UserCreate, UserMe, UserPublic
from models.schemas.auth_schema import Token
from models.db_models.table_models import User
from services.auth.auth_service_exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError
)
from datetime import datetime


@pytest.fixture
def mock_session():
    """Fixture for mocked database session."""
    return Mock()


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_auth_service():
    """Fixture for mocked auth service."""
    return Mock()


@pytest.fixture
def sample_user():
    """Fixture for sample user."""
    user = User(
        id=1,
        user_name="testuser",
        email="test@example.com",
        hashed_password="hashed_password_123",
        created_at=datetime.now()
    )
    return user


@pytest.fixture
def sample_user_create():
    """Fixture for sample user creation data."""
    return UserCreate(
        user_name="newuser",
        email="newuser@example.com",
        password="password123"
    )


@pytest.fixture
def sample_token():
    """Fixture for sample token."""
    return Token(
        access_token="sample_access_token_xyz",
        token_type="bearer"
    )


# Tests for register_user function
def test_register_user_success(mock_request, mock_session, mock_auth_service, sample_user_create, sample_user):
    """Test successful user registration."""
    with patch('routes.auth.auth_routes.auth_service', mock_auth_service):
        mock_auth_service.register_user.return_value = sample_user

        result = register_user(mock_request, sample_user_create, mock_session)

        mock_auth_service.register_user.assert_called_once_with(mock_session, sample_user_create)
        assert isinstance(result, UserPublic)
        assert result.id == sample_user.id
        assert result.user_name == sample_user.user_name
        assert result.created_at == sample_user.created_at


def test_register_user_already_exists(mock_request, mock_session, mock_auth_service, sample_user_create):
    """Test user registration raises HTTPException when user already exists."""
    with patch('routes.auth.auth_routes.auth_service', mock_auth_service):
        mock_auth_service.register_user.side_effect = UserAlreadyExistsError("User already exists")

        with pytest.raises(HTTPException) as exc_info:
            register_user(mock_request, sample_user_create, mock_session)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "User already exists."


# Tests for login_for_access_token function
def test_login_success(mock_request, mock_session, mock_auth_service, sample_token):
    """Test successful user login."""
    with patch('routes.auth.auth_routes.auth_service', mock_auth_service):
        mock_auth_service.login.return_value = sample_token

        form_data = Mock(spec=OAuth2PasswordRequestForm)
        form_data.username = "test@example.com"
        form_data.password = "password123"

        result = login_for_access_token(mock_request, form_data, mock_session)

        mock_auth_service.login.assert_called_once_with(
            session=mock_session,
            login="test@example.com",
            password="password123"
        )
        assert isinstance(result, Token)
        assert result.access_token == sample_token.access_token
        assert result.token_type == sample_token.token_type


def test_login_invalid_credentials(mock_request, mock_session, mock_auth_service):
    """Test login raises HTTPException with invalid credentials."""
    with patch('routes.auth.auth_routes.auth_service', mock_auth_service):
        mock_auth_service.login.side_effect = InvalidCredentialsError("Invalid credentials")

        form_data = Mock(spec=OAuth2PasswordRequestForm)
        form_data.username = "wrong@example.com"
        form_data.password = "wrongpassword"

        with pytest.raises(HTTPException) as exc_info:
            login_for_access_token(mock_request, form_data, mock_session)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials."


# Tests for get_my_profile function
def test_get_my_profile_success(mock_request, sample_user):
    """Test successful retrieval of current user profile."""
    result = get_my_profile(mock_request, sample_user)

    assert isinstance(result, UserMe)
    assert result.id == sample_user.id
    assert result.user_name == sample_user.user_name
    assert result.email == sample_user.email


def test_get_my_profile_with_different_user(mock_request):
    """Test get my profile with different user data."""
    user = User(
        id=42,
        user_name="anotheruser",
        email="another@example.com",
        hashed_password="hashed_pass",
        created_at=datetime.now()
    )

    result = get_my_profile(mock_request, user)

    assert isinstance(result, UserMe)
    assert result.id == 42
    assert result.user_name == "anotheruser"
    assert result.email == "another@example.com"
