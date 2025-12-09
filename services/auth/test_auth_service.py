"""
test_auth_service.py

Test for auth service - business logic.
"""
import pytest
import uuid

from services.auth.auth_service import AuthService
from services.auth.auth_service_exceptions import (
    AuthServiceError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    TokenCreationError
)
from models.schemas.user_schema import UserCreate
from models.schemas.auth_schema import Token
from models.db_models.test_db import get_session as get_test_session


def test_register_user():
    """Test to register a new user."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"testuser_{suffix}",
        email=f"test_{suffix}@example.com",
        password="securepassword123"
    )

    user = service.register_user(session, user_data)

    assert user.user_name == f"testuser_{suffix}"
    assert user.email == f"test_{suffix}@example.com"
    assert user.id is not None
    assert user.hashed_password is not None
    assert user.hashed_password != "securepassword123"


def test_register_user_duplicate_email():
    """Test registering a user with duplicate email."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"user1_{suffix}",
        email=f"duplicate_{suffix}@example.com",
        password="password123"
    )
    service.register_user(session, user_data)

    # Try to register another user with the same email
    duplicate_data = UserCreate(
        user_name=f"user2_{suffix}",
        email=f"duplicate_{suffix}@example.com",
        password="password456"
    )

    with pytest.raises(UserAlreadyExistsError):
        service.register_user(session, duplicate_data)


def test_register_user_duplicate_username():
    """Test registering a user with duplicate username."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"duplicate_user_{suffix}",
        email=f"email1_{suffix}@example.com",
        password="password123"
    )
    service.register_user(session, user_data)

    # Try to register another user with the same username
    duplicate_data = UserCreate(
        user_name=f"duplicate_user_{suffix}",
        email=f"email2_{suffix}@example.com",
        password="password456"
    )

    with pytest.raises(UserAlreadyExistsError):
        service.register_user(session, duplicate_data)


def test_login_success():
    """Test successful login with valid credentials."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"loginuser_{suffix}",
        email=f"login_{suffix}@example.com",
        password="mypassword123"
    )
    service.register_user(session, user_data)

    # Login with email
    token = service.login(session, f"login_{suffix}@example.com", "mypassword123")

    assert isinstance(token, Token)
    assert token.access_token is not None
    assert token.token_type == "bearer"


def test_login_with_username():
    """Test successful login using username."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"loginuser_{suffix}",
        email=f"login_{suffix}@example.com",
        password="mypassword123"
    )
    service.register_user(session, user_data)

    # Login with username
    token = service.login(session, f"loginuser_{suffix}", "mypassword123")

    assert isinstance(token, Token)
    assert token.access_token is not None
    assert token.token_type == "bearer"


def test_login_invalid_password():
    """Test login with incorrect password."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"wrongpass_{suffix}",
        email=f"wrongpass_{suffix}@example.com",
        password="correctpassword"
    )
    service.register_user(session, user_data)

    with pytest.raises(InvalidCredentialsError):
        service.login(session, f"wrongpass_{suffix}@example.com", "wrongpassword")


def test_login_user_not_found():
    """Test login with non-existent user."""
    gen = get_test_session()
    session = next(gen)

    service = AuthService()

    suffix = uuid.uuid4().hex[:8]

    with pytest.raises(InvalidCredentialsError):
        service.login(session, f"nonexistent_{suffix}@example.com", "password123")
