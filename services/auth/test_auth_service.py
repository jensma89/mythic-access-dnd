# """
# test_auth_service.py
# 
# Test for auth service - business logic.
# """
# import pytest
# import uuid
# 
# from services.auth.auth_service import AuthService
# from services.auth.auth_service_exceptions import (
#     AuthServiceError,
#     UserAlreadyExistsError,
#     InvalidCredentialsError,
#     TokenCreationError
# )
# from models.schemas.user_schema import UserCreate
# from models.schemas.auth_schema import Token
# from models.db_models.test_db import get_session as get_test_session
# 
# 
# def test_register_user():
#     """Test to register a new user."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"testuser_{suffix}",
#         email=f"test_{suffix}@example.com",
#         password="securepassword123"
#     )
# 
#     user = service.register_user(session, user_data)
# 
#     assert user.user_name == f"testuser_{suffix}"
#     assert user.email == f"test_{suffix}@example.com"
#     assert user.id is not None
#     assert user.hashed_password is not None
#     assert user.hashed_password != "securepassword123"
# 
# 
# def test_register_user_duplicate_email():
#     """Test registering a user with duplicate email."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"user1_{suffix}",
#         email=f"duplicate_{suffix}@example.com",
#         password="password123"
#     )
#     service.register_user(session, user_data)
# 
#     # Try to register another user with the same email
#     duplicate_data = UserCreate(
#         user_name=f"user2_{suffix}",
#         email=f"duplicate_{suffix}@example.com",
#         password="password456"
#     )
# 
#     with pytest.raises(UserAlreadyExistsError):
#         service.register_user(session, duplicate_data)
# 
# 
# def test_register_user_duplicate_username():
#     """Test registering a user with duplicate username."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"duplicate_user_{suffix}",
#         email=f"email1_{suffix}@example.com",
#         password="password123"
#     )
#     service.register_user(session, user_data)
# 
#     # Try to register another user with the same username
#     duplicate_data = UserCreate(
#         user_name=f"duplicate_user_{suffix}",
#         email=f"email2_{suffix}@example.com",
#         password="password456"
#     )
# 
#     with pytest.raises(UserAlreadyExistsError):
#         service.register_user(session, duplicate_data)
# 
# 
# def test_login_success():
#     """Test successful login with valid credentials."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"loginuser_{suffix}",
#         email=f"login_{suffix}@example.com",
#         password="mypassword123"
#     )
#     service.register_user(session, user_data)
# 
#     # Login with email
#     token = service.login(session, f"login_{suffix}@example.com", "mypassword123")
# 
#     assert isinstance(token, Token)
#     assert token.access_token is not None
#     assert token.token_type == "bearer"
# 
# 
# def test_login_with_username():
#     """Test successful login using username."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"loginuser_{suffix}",
#         email=f"login_{suffix}@example.com",
#         password="mypassword123"
#     )
#     service.register_user(session, user_data)
# 
#     # Login with username
#     token = service.login(session, f"loginuser_{suffix}", "mypassword123")
# 
#     assert isinstance(token, Token)
#     assert token.access_token is not None
#     assert token.token_type == "bearer"
# 
# 
# def test_login_invalid_password():
#     """Test login with incorrect password."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"wrongpass_{suffix}",
#         email=f"wrongpass_{suffix}@example.com",
#         password="correctpassword"
#     )
#     service.register_user(session, user_data)
# 
#     with pytest.raises(InvalidCredentialsError):
#         service.login(session, f"wrongpass_{suffix}@example.com", "wrongpassword")
# 
# 
# def test_login_user_not_found():
#     """Test login with non-existent user."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = AuthService()
# 
#     suffix = uuid.uuid4().hex[:8]
# 
#     with pytest.raises(InvalidCredentialsError):
#         service.login(session, f"nonexistent_{suffix}@example.com", "password123")


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock, patch
from services.auth.auth_service import AuthService
from services.auth.auth_service_exceptions import (
    AuthServiceError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    TokenCreationError
)
from models.schemas.user_schema import UserCreate
from models.schemas.auth_schema import Token
from models.db_models.table_models import User


@pytest.fixture
def mock_session():
    """Fixture for mocked database session."""
    return Mock()


@pytest.fixture
def auth_service():
    """Fixture for AuthService instance."""
    return AuthService()


@pytest.fixture
def sample_user_data():
    """Fixture for sample user registration data."""
    return UserCreate(
        user_name="testuser",
        email="test@example.com",
        password="securepassword123"
    )


@pytest.fixture
def sample_user():
    """Fixture for sample User model."""
    user = User(
        user_name="testuser",
        email="test@example.com",
        hashed_password="hashed_password_value"
    )
    user.id = 1
    return user


# Tests for register_user function
def test_register_user_success(auth_service, mock_session, sample_user_data):
    """Test successful user registration."""
    mock_session.exec.return_value.first.return_value = None
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(side_effect=lambda user: setattr(user, 'id', 1))

    with patch('services.auth.auth_service.hash_password', return_value="hashed_password"):
        result = auth_service.register_user(mock_session, sample_user_data)

        mock_session.exec.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

        assert result.user_name == sample_user_data.user_name
        assert result.email == sample_user_data.email
        assert result.hashed_password == "hashed_password"


def test_register_user_duplicate_email(auth_service, mock_session, sample_user_data, sample_user):
    """Test registration fails when email already exists."""
    mock_session.exec.return_value.first.return_value = sample_user

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        auth_service.register_user(mock_session, sample_user_data)

    assert "already exists" in str(exc_info.value)


def test_register_user_duplicate_username(auth_service, mock_session):
    """Test registration fails when username already exists."""
    existing_user = User(
        user_name="testuser",
        email="different@example.com",
        hashed_password="hashed"
    )
    existing_user.id = 2

    mock_session.exec.return_value.first.return_value = existing_user

    user_data = UserCreate(
        user_name="testuser",
        email="new@example.com",
        password="password123"
    )

    with pytest.raises(UserAlreadyExistsError):
        auth_service.register_user(mock_session, user_data)


def test_register_user_database_error_on_duplicate_check(auth_service, mock_session, sample_user_data):
    """Test registration handles database error during duplicate check."""
    mock_session.exec.side_effect = Exception("Database error")

    with pytest.raises(AuthServiceError) as exc_info:
        auth_service.register_user(mock_session, sample_user_data)

    assert "checking duplicates" in str(exc_info.value)


def test_register_user_database_error_on_creation(auth_service, mock_session, sample_user_data):
    """Test registration handles database error during user creation."""
    mock_session.exec.return_value.first.return_value = None
    mock_session.add = Mock()
    mock_session.commit = Mock(side_effect=Exception("Database error"))

    with patch('services.auth.auth_service.hash_password', return_value="hashed_password"):
        with pytest.raises(AuthServiceError) as exc_info:
            auth_service.register_user(mock_session, sample_user_data)

        assert "storing user" in str(exc_info.value)


def test_register_user_hashes_password(auth_service, mock_session, sample_user_data):
    """Test that password is properly hashed during registration."""
    mock_session.exec.return_value.first.return_value = None
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    with patch('services.auth.auth_service.hash_password', return_value="super_hashed_password") as mock_hash:
        auth_service.register_user(mock_session, sample_user_data)

        mock_hash.assert_called_once_with(sample_user_data.password)


# Tests for login function
def test_login_success(auth_service, mock_session, sample_user):
    """Test successful login with valid credentials."""
    with patch('services.auth.auth_service.authenticate_user', return_value=sample_user):
        with patch('services.auth.auth_service.create_access_token', return_value="test_token_123"):
            with patch('services.auth.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES', 30):
                token = auth_service.login(mock_session, "test@example.com", "password123")

                assert isinstance(token, Token)
                assert token.access_token == "test_token_123"
                assert token.token_type == "bearer"


def test_login_invalid_credentials(auth_service, mock_session):
    """Test login fails with invalid credentials."""
    with patch('services.auth.auth_service.authenticate_user', return_value=None):
        with pytest.raises(InvalidCredentialsError) as exc_info:
            auth_service.login(mock_session, "test@example.com", "wrongpassword")

        assert "Incorrect email or password" in str(exc_info.value)


def test_login_authentication_error(auth_service, mock_session):
    """Test login handles authentication error."""
    with patch('services.auth.auth_service.authenticate_user', side_effect=Exception("Auth error")):
        with pytest.raises(AuthServiceError) as exc_info:
            auth_service.login(mock_session, "test@example.com", "password123")

        assert "authentication" in str(exc_info.value)


def test_login_token_creation_error(auth_service, mock_session, sample_user):
    """Test login handles token creation error."""
    with patch('services.auth.auth_service.authenticate_user', return_value=sample_user):
        with patch('services.auth.auth_service.create_access_token', side_effect=Exception("Token error")):
            with pytest.raises(TokenCreationError) as exc_info:
                auth_service.login(mock_session, "test@example.com", "password123")

            assert "access token" in str(exc_info.value)


def test_login_creates_token_with_user_email(auth_service, mock_session, sample_user):
    """Test that login creates token with user's email as subject."""
    with patch('services.auth.auth_service.authenticate_user', return_value=sample_user):
        with patch('services.auth.auth_service.create_access_token', return_value="token") as mock_create:
            with patch('services.auth.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES', 30):
                auth_service.login(mock_session, "test@example.com", "password123")

                call_args = mock_create.call_args
                assert call_args[1]['data']['sub'] == sample_user.email


def test_login_uses_correct_token_expiration(auth_service, mock_session, sample_user):
    """Test that login uses correct token expiration time."""
    with patch('services.auth.auth_service.authenticate_user', return_value=sample_user):
        with patch('services.auth.auth_service.create_access_token', return_value="token") as mock_create:
            with patch('services.auth.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES', 60):
                auth_service.login(mock_session, "test@example.com", "password123")

                call_args = mock_create.call_args
                expires_delta = call_args[1]['expires_delta']
                assert expires_delta.total_seconds() == 60 * 60


def test_login_passes_credentials_to_authenticate(auth_service, mock_session, sample_user):
    """Test that login passes correct credentials to authenticate_user."""
    with patch('services.auth.auth_service.authenticate_user', return_value=sample_user) as mock_auth:
        with patch('services.auth.auth_service.create_access_token', return_value="token"):
            auth_service.login(mock_session, "user@test.com", "mypassword")

            mock_auth.assert_called_once_with(
                session=mock_session,
                login="user@test.com",
                password="mypassword"
            )
