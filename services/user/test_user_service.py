"""
test_user_service.py

Test for user service - business logic.
"""
import pytest

from services.user.user_service import UserService
from services.user.user_service_exceptions import (
    UserNotFoundError,
    UserCreateError,
    UserUpdateError,
    UserDeleteError
)
from models.schemas.user_schema import UserCreate, UserUpdate
from models.db_models.test_db import get_session as get_test_session
from repositories.sql_user_repository import SqlAlchemyUserRepository
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from dependencies import UserQueryParams
from auth.test_helpers import create_test_user


@pytest.fixture(scope="function")
def db_session():
    """Fixture to provide a test database session with proper cleanup."""
    gen = get_test_session()
    session = next(gen)
    yield session
    try:
        next(gen)
    except StopIteration:
        pass


def test_create_user(db_session):
    """Test to create a new user."""
    import uuid
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"test_service_user_{suffix}",
        email=f"testservice_{suffix}@example.com",
        password="password123"
    )
    user = service.create_user(user_data)

    assert user.user_name == f"test_service_user_{suffix}"
    assert user.id is not None


def test_get_user(db_session):
    """Test to get a user by ID."""
    user = create_test_user(db_session)

    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    result = service.get_user(user.id)

    assert result.id == user.id
    assert result.user_name == user.user_name


def test_get_user_not_found(db_session):
    """Test get user with non-existent ID."""
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    with pytest.raises(UserNotFoundError):
        service.get_user(99999)


def test_list_users(db_session):
    """Test to list all users."""
    create_test_user(db_session)
    create_test_user(db_session)

    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    filters = UserQueryParams()
    users = service.list_users(filters)

    assert isinstance(users, list)


def test_list_users_with_filter(db_session):
    """Test list users with name filter."""
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    service.create_user(UserCreate(
        user_name="filtered_user",
        email="filtered@example.com",
        password="password123"
    ))

    filters = UserQueryParams(name="filtered")
    users = service.list_users(filters)

    assert len(users) >= 1
    assert any("filtered" in u.user_name for u in users)


def test_update_user(db_session):
    """Test to update a user."""
    import uuid
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    # Create user via service to ensure same session
    suffix = uuid.uuid4().hex[:8]
    user_data = UserCreate(
        user_name=f"update_test_{suffix}",
        email=f"update_{suffix}@test.com",
        password="password123"
    )
    user = service.create_user(user_data)

    # Update with unique name
    new_suffix = uuid.uuid4().hex[:8]
    update_data = UserUpdate(user_name=f"updated_name_{new_suffix}")
    updated = service.update_user(user.id, update_data)

    assert updated is not None
    assert updated.id == user.id


def test_update_user_not_found(db_session):
    """Test update with non-existent user ID."""
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    update_data = UserUpdate(user_name="new_name")

    with pytest.raises(UserNotFoundError):
        service.update_user(99999, update_data)


def test_delete_user(db_session):
    """Test to delete a user."""
    user = create_test_user(db_session)

    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    deleted = service.delete_user(user.id)

    assert deleted.id == user.id
    assert deleted.user_name == user.user_name

    # Verify user is gone
    with pytest.raises(UserNotFoundError):
        service.get_user(user.id)


def test_delete_user_not_found(db_session):
    """Test delete with non-existent user ID."""
    service = UserService(
        user_repo=SqlAlchemyUserRepository(db_session),
        campaign_repo=SqlAlchemyCampaignRepository(db_session),
        class_repo=SqlAlchemyClassRepository(db_session),
        diceset_repo=SqlAlchemyDiceSetRepository(db_session),
        dicelog_repo=SqlAlchemyDiceLogRepository(db_session)
    )

    with pytest.raises((UserNotFoundError, UserDeleteError)):
        service.delete_user(99999)
