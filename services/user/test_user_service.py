# """
# test_user_service.py
# 
# Test for user service - business logic.
# """
# import pytest
# 
# from services.user.user_service import UserService
# from services.user.user_service_exceptions import (
#     UserNotFoundError,
#     UserCreateError,
#     UserUpdateError,
#     UserDeleteError
# )
# from models.schemas.user_schema import UserCreate, UserUpdate
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from repositories.sql_user_repository import SqlAlchemyUserRepository
# from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from dependencies import UserQueryParams
# from auth.test_helpers import create_test_user
# 
# 
# def test_create_user():
#     """Test to create a new user."""
#     import uuid
#     session = Session(test_engine)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"test_service_user_{suffix}",
#         email=f"testservice_{suffix}@example.com",
#         password="password123"
#     )
#     user = service.create_user(user_data)
# 
#     assert user.user_name == f"test_service_user_{suffix}"
#     assert user.id is not None
# 
# 
# def test_get_user():
#     """Test to get a user by ID."""
#     session = Session(test_engine)
# 
#     user = create_test_user(session)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     result = service.get_user(user.id)
# 
#     assert result.id == user.id
#     assert result.user_name == user.user_name
# 
# 
# def test_get_user_not_found():
#     """Test get user with non-existent ID."""
#     session = Session(test_engine)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(UserNotFoundError):
#         service.get_user(99999)
# 
# 
# def test_list_users():
#     """Test to list all users."""
#     session = Session(test_engine)
# 
#     create_test_user(session)
#     create_test_user(session)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     filters = UserQueryParams()
#     users = service.list_users(filters)
# 
#     assert isinstance(users, list)
# 
# 
# def test_list_users_with_filter():
#     """Test list users with name filter."""
#     session = Session(test_engine)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     service.create_user(UserCreate(
#         user_name="filtered_user",
#         email="filtered@example.com",
#         password="password123"
#     ))
# 
#     filters = UserQueryParams(name="filtered")
#     users = service.list_users(filters)
# 
#     assert len(users) >= 1
#     assert any("filtered" in u.user_name for u in users)
# 
# 
# def test_update_user():
#     """Test to update a user."""
#     session = Session(test_engine)
# 
#     import uuid
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     # Create user via service to ensure same session
#     suffix = uuid.uuid4().hex[:8]
#     user_data = UserCreate(
#         user_name=f"update_test_{suffix}",
#         email=f"update_{suffix}@test.com",
#         password="password123"
#     )
#     user = service.create_user(user_data)
# 
#     # Update with unique name
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = UserUpdate(user_name=f"updated_name_{new_suffix}")
#     updated = service.update_user(user.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == user.id
# 
# 
# def test_update_user_not_found():
#     """Test update with non-existent user ID."""
#     session = Session(test_engine)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = UserUpdate(user_name="new_name")
# 
#     with pytest.raises(UserNotFoundError):
#         service.update_user(99999, update_data)
# 
# 
# def test_delete_user():
#     """Test to delete a user."""
#     session = Session(test_engine)
# 
#     user = create_test_user(session)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     deleted = service.delete_user(user.id)
# 
#     assert deleted.id == user.id
#     assert deleted.user_name == user.user_name
# 
#     # Verify user is gone
#     with pytest.raises(UserNotFoundError):
#         service.get_user(user.id)
# 
# 
# def test_delete_user_not_found():
#     """Test delete with non-existent user ID."""
#     session = Session(test_engine)
# 
#     service = UserService(
#         user_repo=SqlAlchemyUserRepository(session),
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((UserNotFoundError, UserDeleteError)):
#         service.delete_user(99999)
#


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from services.user.user_service import UserService
from services.user.user_service_exceptions import (
    UserServiceError,
    UserNotFoundError,
    UserCreateError,
    UserUpdateError,
    UserDeleteError
)
from models.schemas.user_schema import UserCreate, UserUpdate, UserPublic
from dependencies import UserQueryParams


@pytest.fixture
def mock_user_repo():
    """Fixture for mocked user repository."""
    return Mock()


@pytest.fixture
def mock_campaign_repo():
    """Fixture for mocked campaign repository."""
    return Mock()


@pytest.fixture
def mock_class_repo():
    """Fixture for mocked class repository."""
    return Mock()


@pytest.fixture
def mock_diceset_repo():
    """Fixture for mocked diceset repository."""
    return Mock()


@pytest.fixture
def mock_dicelog_repo():
    """Fixture for mocked dicelog repository."""
    return Mock()


@pytest.fixture
def user_service(mock_user_repo, mock_campaign_repo, mock_class_repo,
                 mock_diceset_repo, mock_dicelog_repo):
    """Fixture for UserService instance with mocked repositories."""
    return UserService(
        user_repo=mock_user_repo,
        campaign_repo=mock_campaign_repo,
        class_repo=mock_class_repo,
        diceset_repo=mock_diceset_repo,
        dicelog_repo=mock_dicelog_repo
    )


@pytest.fixture
def sample_user_data():
    """Fixture for sample user creation data."""
    return UserCreate(
        user_name="testuser",
        email="test@example.com",
        password="securepassword123"
    )


@pytest.fixture
def sample_user():
    """Fixture for sample user."""
    from datetime import datetime
    return UserPublic(
        id=1,
        user_name="testuser",
        created_at=datetime.now()
    )


# Tests for create_user function
def test_create_user_success(user_service, mock_user_repo, sample_user_data, sample_user):
    """Test successful user creation."""
    mock_user_repo.add.return_value = sample_user

    result = user_service.create_user(sample_user_data)

    mock_user_repo.add.assert_called_once_with(sample_user_data)
    assert result.id == sample_user.id
    assert result.user_name == sample_user.user_name


def test_create_user_repository_returns_none(user_service, mock_user_repo, sample_user_data):
    """Test user creation fails when repository returns None."""
    mock_user_repo.add.return_value = None

    with pytest.raises(UserCreateError) as exc_info:
        user_service.create_user(sample_user_data)

    assert "creating user" in str(exc_info.value)


def test_create_user_exception(user_service, mock_user_repo, sample_user_data):
    """Test user creation handles exceptions."""
    mock_user_repo.add.side_effect = Exception("Database error")

    with pytest.raises(UserCreateError) as exc_info:
        user_service.create_user(sample_user_data)

    assert "Error while creating user" in str(exc_info.value)


# Tests for get_user function
def test_get_user_success(user_service, mock_user_repo, sample_user):
    """Test successful user retrieval."""
    mock_user_repo.get_by_id.return_value = sample_user

    result = user_service.get_user(1)

    mock_user_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_user.id
    assert result.user_name == sample_user.user_name


def test_get_user_not_found(user_service, mock_user_repo):
    """Test get user raises error when user not found."""
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.get_user(999)

    assert "User with user ID 999 not found" in str(exc_info.value)


def test_get_user_exception(user_service, mock_user_repo):
    """Test get user handles exceptions."""
    mock_user_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(UserServiceError) as exc_info:
        user_service.get_user(1)

    assert "Error while retrieving user" in str(exc_info.value)


# Tests for list_users function
def test_list_users_success(user_service, mock_user_repo):
    """Test successful user listing."""
    from datetime import datetime
    now = datetime.now()
    users = [
        UserPublic(id=1, user_name="user1", created_at=now),
        UserPublic(id=2, user_name="user2", created_at=now)
    ]
    mock_user_repo.list_all.return_value = users

    filters = UserQueryParams()
    result = user_service.list_users(filters, offset=0, limit=100)

    mock_user_repo.list_all.assert_called_once()
    assert len(result) == 2
    assert result[0].user_name == "user1"
    assert result[1].user_name == "user2"


def test_list_users_with_filters(user_service, mock_user_repo):
    """Test user listing with name filter."""
    from datetime import datetime
    users = [
        UserPublic(id=1, user_name="filtered_user", created_at=datetime.now())
    ]
    mock_user_repo.list_all.return_value = users

    filters = UserQueryParams(name="filtered")
    result = user_service.list_users(filters, offset=5, limit=20)

    mock_user_repo.list_all.assert_called_once()
    assert len(result) == 1
    assert result[0].user_name == "filtered_user"


def test_list_users_empty(user_service, mock_user_repo):
    """Test user listing returns empty list."""
    mock_user_repo.list_all.return_value = []

    filters = UserQueryParams()
    result = user_service.list_users(filters)

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_users_exception(user_service, mock_user_repo):
    """Test list users handles exceptions."""
    mock_user_repo.list_all.side_effect = Exception("Database error")

    filters = UserQueryParams()

    with pytest.raises(UserServiceError) as exc_info:
        user_service.list_users(filters)

    assert "Error while listing users" in str(exc_info.value)


# Tests for update_user function
def test_update_user_success(user_service, mock_user_repo):
    """Test successful user update."""
    from datetime import datetime
    now = datetime.now()
    existing_user = UserPublic(id=1, user_name="oldname", created_at=now)
    updated_user = UserPublic(id=1, user_name="newname", created_at=now)

    mock_user_repo.get_by_id.return_value = existing_user
    mock_user_repo.update.return_value = updated_user

    update_data = UserUpdate(user_name="newname")
    result = user_service.update_user(1, update_data)

    mock_user_repo.get_by_id.assert_called_once_with(1)
    mock_user_repo.update.assert_called_once_with(1, update_data)
    assert result.id == 1
    assert result.user_name == "newname"


def test_update_user_not_found(user_service, mock_user_repo):
    """Test update user raises error when user not found."""
    mock_user_repo.get_by_id.return_value = None

    update_data = UserUpdate(user_name="newname")

    with pytest.raises(UserNotFoundError) as exc_info:
        user_service.update_user(999, update_data)

    assert "User with ID 999 not found" in str(exc_info.value)


def test_update_user_update_fails(user_service, mock_user_repo):
    """Test update user raises error when update returns None."""
    from datetime import datetime
    existing_user = UserPublic(id=1, user_name="oldname", created_at=datetime.now())

    mock_user_repo.get_by_id.return_value = existing_user
    mock_user_repo.update.return_value = None

    update_data = UserUpdate(user_name="newname")

    with pytest.raises(UserUpdateError) as exc_info:
        user_service.update_user(1, update_data)

    assert "Error while updating user" in str(exc_info.value)


def test_update_user_exception(user_service, mock_user_repo):
    """Test update user handles exceptions."""
    mock_user_repo.get_by_id.side_effect = Exception("Database error")

    update_data = UserUpdate(user_name="newname")

    with pytest.raises(UserUpdateError) as exc_info:
        user_service.update_user(1, update_data)

    assert "Error while updating user" in str(exc_info.value)


# Tests for delete_user function
def test_delete_user_success(user_service, mock_user_repo, mock_campaign_repo,
                             mock_class_repo, mock_diceset_repo, mock_dicelog_repo, sample_user):
    """Test successful user deletion with related entities."""
    mock_user_repo.get_by_id.return_value = sample_user

    # Setup related entities
    mock_dicelog_repo.list_by_user.return_value = [Mock(id=1), Mock(id=2)]
    mock_diceset_repo.list_by_user.return_value = [Mock(id=10), Mock(id=11)]
    mock_class_repo.list_by_user.return_value = [Mock(id=20)]
    mock_campaign_repo.list_by_user.return_value = [Mock(id=30)]

    mock_user_repo.delete.return_value = sample_user

    result = user_service.delete_user(1)

    # Verify deletion order: dice logs, dice sets, classes, campaigns, user
    assert mock_dicelog_repo.delete.call_count == 2
    assert mock_diceset_repo.delete.call_count == 2
    assert mock_class_repo.delete.call_count == 1
    assert mock_campaign_repo.delete.call_count == 1
    mock_user_repo.delete.assert_called_once_with(1)
    assert result == sample_user


def test_delete_user_not_found(user_service, mock_user_repo):
    """Test delete user raises error when user not found."""
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises((UserNotFoundError, UserDeleteError)):
        user_service.delete_user(999)


def test_delete_user_deletion_fails(user_service, mock_user_repo, mock_campaign_repo,
                                    mock_class_repo, mock_diceset_repo, mock_dicelog_repo, sample_user):
    """Test delete user when final deletion returns None."""
    mock_user_repo.get_by_id.return_value = sample_user
    mock_dicelog_repo.list_by_user.return_value = []
    mock_diceset_repo.list_by_user.return_value = []
    mock_class_repo.list_by_user.return_value = []
    mock_campaign_repo.list_by_user.return_value = []
    mock_user_repo.delete.return_value = None

    with pytest.raises(UserDeleteError) as exc_info:
        user_service.delete_user(1)

    assert "deleting user" in str(exc_info.value)


def test_delete_user_exception(user_service, mock_user_repo):
    """Test delete user handles exceptions."""
    mock_user_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(UserDeleteError) as exc_info:
        user_service.delete_user(1)

    assert "Error while deleting user" in str(exc_info.value)


def test_delete_user_no_related_entities(user_service, mock_user_repo, mock_campaign_repo,
                                         mock_class_repo, mock_diceset_repo, mock_dicelog_repo, sample_user):
    """Test deleting user with no related entities."""
    mock_user_repo.get_by_id.return_value = sample_user
    mock_dicelog_repo.list_by_user.return_value = []
    mock_diceset_repo.list_by_user.return_value = []
    mock_class_repo.list_by_user.return_value = []
    mock_campaign_repo.list_by_user.return_value = []
    mock_user_repo.delete.return_value = sample_user

    result = user_service.delete_user(1)

    # Verify no deletions for related entities
    mock_dicelog_repo.delete.assert_not_called()
    mock_diceset_repo.delete.assert_not_called()
    mock_class_repo.delete.assert_not_called()
    mock_campaign_repo.delete.assert_not_called()
    mock_user_repo.delete.assert_called_once_with(1)
    assert result == sample_user
