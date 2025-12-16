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
