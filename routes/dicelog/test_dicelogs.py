# """
# test_dicelogs.py
# 
# Tests for dicelog endpoints.
# """
# from fastapi.testclient import TestClient
# from datetime import datetime, timezone
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from models.schemas.dicelog_schema import DiceLogCreate
# from models.schemas.dice_schema import DiceCreate
# from models.schemas.diceset_schema import DiceSetCreate
# from models.schemas.class_schema import ClassCreate, ClassSkills
# from services.dice.dice_service import DiceService
# from services.diceset.diceset_service import DiceSetService
# from services.dnd_class.class_service import ClassService
# 
# 
# # Override DB dependency
# app.dependency_overrides[prod_get_session] = get_test_session
# 
# 
# def auth_header(user):
#     """Create the authentication header for a user."""
#     token = get_test_token(user)
#     return {"Authorization": f"Bearer {token}"}
# 
# 
# def get_dicelog_repo(session):
#     """Factory to create DiceLogRepository with test session."""
#     return SqlAlchemyDiceLogRepository(session)
# 
# 
# def get_dice_service(session):
#     """Factory to create DiceService with test session."""
#     return DiceService(
#         SqlAlchemyDiceRepository(session),
#         SqlAlchemyDiceLogRepository(session)
#     )
# 
# 
# def get_diceset_service(session):
#     """Factory to create DiceSetService with test session."""
#     return DiceSetService(
#         SqlAlchemyDiceRepository(session),
#         SqlAlchemyDiceSetRepository(session),
#         SqlAlchemyDiceLogRepository(session)
#     )
# 
# 
# def get_class_service(session):
#     """Factory to create ClassService with test session."""
#     return ClassService(
#         SqlAlchemyClassRepository(session),
#         SqlAlchemyDiceSetRepository(session),
#         SqlAlchemyDiceLogRepository(session)
#     )
# 
# 
# def create_test_dice(session, name="D6", sides=6):
#     """Create a test dice."""
#     service = get_dice_service(session)
#     payload = DiceCreate(name=name, sides=sides)
#     return service.create_dice(payload)
# 
# 
# def create_test_diceset(session, user, dnd_class, campaign, name="TestSet", dice_ids=None):
#     """Create a test diceset."""
#     service = get_diceset_service(session)
#     payload = DiceSetCreate(
#         name=name,
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id,
#         dice_ids=dice_ids or []
#     )
#     payload.set_user(user.id)
#     return service.create_diceset(payload)
# 
# 
# def create_test_dicelog(session, user, campaign, dnd_class, diceset=None, roll="D6: 4", result=4):
#     """Create a test dice log entry directly in the repository."""
#     repo = get_dicelog_repo(session)
#     log_entry = DiceLogCreate(
#         user_id=user.id,
#         campaign_id=campaign.id,
#         dnd_class_id=dnd_class.id,
#         diceset_id=diceset.id if diceset else None,
#         roll=roll,
#         result=result,
#         timestamp=datetime.now(timezone.utc)
#     )
#     return repo.log_roll(log_entry)
# 
# 
# def test_list_logs_empty():
#     """Test listing logs when there are none."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         "/dicelogs/",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     # User should have no logs yet
#     assert len(data) == 0
# 
# 
# def test_list_logs_with_entries():
#     """Test listing logs when entries exist."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create class
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar",
#         dnd_class="Warrior",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(user.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create some log entries
#     create_test_dicelog(session, user, campaign, dnd_class, roll="D6: 3", result=3)
#     create_test_dicelog(session, user, campaign, dnd_class, roll="D8: 5", result=5)
#     create_test_dicelog(session, user, campaign, dnd_class, roll="D20: 15", result=15)
# 
#     response = client.get(
#         "/dicelogs/",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) >= 3
# 
# 
# def test_list_logs_pagination():
#     """Test pagination for dice logs."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create class
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar2",
#         dnd_class="Mage",
#         race="Elf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(user.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create multiple log entries
#     for i in range(10):
#         create_test_dicelog(
#             session, user, campaign, dnd_class,
#             roll=f"D20: {i+1}", result=i+1
#         )
# 
#     # Test pagination with limit
#     response = client.get(
#         "/dicelogs/?offset=0&limit=5",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) <= 5
# 
#     # Test pagination with offset
#     response = client.get(
#         "/dicelogs/?offset=5&limit=5",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
# 
# 
# def test_list_logs_only_own():
#     """Test that users only see their own logs."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user1 = create_test_user(session)
#     user2 = create_test_user(session)
#     campaign1 = create_test_campaign(session, user1)
#     campaign2 = create_test_campaign(session, user2)
#     # Create class for user1
#     class_service = get_class_service(session)
#     class_payload1 = ClassCreate(
#         name="TestChar3",
#         dnd_class="Rogue",
#         race="Halfling",
#         campaign_id=campaign1.id,
#         skills=ClassSkills()
#     )
#     class_payload1.set_user(user1.id)
#     dnd_class1 = class_service.create_class(class_payload1)
# 
#     # Create class for user2
#     class_payload2 = ClassCreate(
#         name="TestChar4",
#         dnd_class="Paladin",
#         race="Human",
#         campaign_id=campaign2.id,
#         skills=ClassSkills()
#     )
#     class_payload2.set_user(user2.id)
#     dnd_class2 = class_service.create_class(class_payload2)
# 
#     # Create logs for both users
#     create_test_dicelog(session, user1, campaign1, dnd_class1, roll="User1: D6", result=3)
#     create_test_dicelog(session, user2, campaign2, dnd_class2, roll="User2: D8", result=5)
# 
#     # User1 should only see their own logs
#     response = client.get(
#         "/dicelogs/",
#         headers=auth_header(user1)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     for log in data:
#         assert log["user_id"] == user1.id
# 
# 
# def test_get_log_success():
#     """Test getting a single log by ID."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create class
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar5",
#         dnd_class="Ranger",
#         race="Elf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(user.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create a log entry
#     log = create_test_dicelog(session, user, campaign, dnd_class, roll="D20: 18", result=18)
# 
#     response = client.get(
#         f"/dicelogs/{log.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == log.id
#     assert data["user_id"] == user.id
#     assert data["result"] == 18
# 
# 
# def test_get_log_not_found():
#     """Test getting a non-existing log returns 404."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         "/dicelogs/99999",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"].lower()
# 
# 
# def test_get_log_forbidden():
#     """Test that accessing another user's log is forbidden."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     campaign = create_test_campaign(session, owner)
#     # Create class for owner
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar6",
#         dnd_class="Bard",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(owner.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create a log entry for owner
#     log = create_test_dicelog(session, owner, campaign, dnd_class, roll="D6: 4", result=4)
# 
#     # Try to access as other user
#     response = client.get(
#         f"/dicelogs/{log.id}",
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
#     assert "not allowed" in response.json()["detail"].lower()
# 
# 
# def test_list_logs_with_diceset():
#     """Test that logs with diceset_id are returned correctly."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create class
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar7",
#         dnd_class="Cleric",
#         race="Dwarf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(user.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create dice and diceset
#     d6 = create_test_dice(session, "D6", 6)
#     diceset = create_test_diceset(
#         session, user, dnd_class, campaign, "TestSet", [d6.id]
#     )
# 
#     # Create log with diceset reference
#     create_test_dicelog(
#         session, user, campaign, dnd_class,
#         diceset=diceset, roll="TestSet: [4]", result=4
#     )
# 
#     response = client.get(
#         "/dicelogs/",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     # Find the log with our diceset
#     diceset_logs = [log for log in data if log.get("diceset_id") == diceset.id]
#     assert len(diceset_logs) >= 1
#     assert diceset_logs[0]["diceset_id"] == diceset.id
# 
# 
# def test_list_logs_with_single_dice():
#     """Test that logs without diceset_id (single dice rolls) work correctly."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create class
#     class_service = get_class_service(session)
#     class_payload = ClassCreate(
#         name="TestChar8",
#         dnd_class="Monk",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     class_payload.set_user(user.id)
#     dnd_class = class_service.create_class(class_payload)
# 
#     # Create log without diceset (single dice roll)
#     create_test_dicelog(
#         session, user, campaign, dnd_class,
#         diceset=None, roll="D20: 15", result=15
#     )
# 
#     response = client.get(
#         "/dicelogs/",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     # Find logs without diceset
#     single_dice_logs = [log for log in data if log.get("diceset_id") is None]
#     assert len(single_dice_logs) >= 1
#


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from fastapi import HTTPException, Request
from routes.dicelog.dicelogs import list_logs, get_log
from models.schemas.dicelog_schema import DiceLogPublic
from models.db_models.table_models import User
from dependencies import Pagination
from datetime import datetime


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_repo():
    """Fixture for mocked dicelog repository."""
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
def mock_other_user():
    """Fixture for mocked other user."""
    user = User(
        id=2,
        user_name="otheruser",
        email="other@example.com",
        hashed_password="hashed_password",
        created_at=datetime.now()
    )
    return user


@pytest.fixture
def sample_dicelog():
    """Fixture for sample dice log."""
    return DiceLogPublic(
        id=1,
        user_id=1,
        campaign_id=10,
        dnd_class_id=5,
        diceset_id=None,
        roll="D20: 15",
        result=15,
        timestamp=datetime.now()
    )


@pytest.fixture
def mock_pagination():
    """Fixture for mocked pagination."""
    return Pagination(offset=0, limit=100)


# Tests for list_logs function
def test_list_logs_success(mock_request, mock_user, mock_pagination, mock_repo):
    """Test successful dice logs list retrieval."""
    logs = [
        DiceLogPublic(id=1, user_id=1, campaign_id=10, dnd_class_id=5, diceset_id=None, roll="D6: 3", result=3, timestamp=datetime.now()),
        DiceLogPublic(id=2, user_id=1, campaign_id=10, dnd_class_id=5, diceset_id=None, roll="D20: 15", result=15, timestamp=datetime.now()),
        DiceLogPublic(id=3, user_id=1, campaign_id=10, dnd_class_id=5, diceset_id=2, roll="Set: [4,6]", result=10, timestamp=datetime.now())
    ]
    mock_repo.list_logs.return_value = logs

    result = list_logs(mock_request, mock_user, mock_pagination, mock_repo)

    mock_repo.list_logs.assert_called_once_with(
        user_id=mock_user.id,
        offset=0,
        limit=100
    )
    assert len(result) == 3
    assert result[0].roll == "D6: 3"
    assert result[1].roll == "D20: 15"
    assert result[2].diceset_id == 2


def test_list_logs_empty(mock_request, mock_user, mock_pagination, mock_repo):
    """Test dice logs list returns empty list."""
    mock_repo.list_logs.return_value = []

    result = list_logs(mock_request, mock_user, mock_pagination, mock_repo)

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_logs_exception(mock_request, mock_user, mock_pagination, mock_repo):
    """Test list logs raises HTTPException on generic error."""
    mock_repo.list_logs.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc_info:
        list_logs(mock_request, mock_user, mock_pagination, mock_repo)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error while listing dice logs."


def test_list_logs_with_pagination(mock_request, mock_user, mock_repo):
    """Test dice logs list with custom pagination."""
    custom_pagination = Pagination(offset=10, limit=5)
    mock_repo.list_logs.return_value = []

    list_logs(mock_request, mock_user, custom_pagination, mock_repo)

    mock_repo.list_logs.assert_called_once_with(
        user_id=mock_user.id,
        offset=10,
        limit=5
    )


# Tests for get_log function
def test_get_log_success(mock_request, mock_user, mock_repo, sample_dicelog):
    """Test successful dice log retrieval."""
    mock_repo.get_by_id.return_value = sample_dicelog

    result = get_log(mock_request, 1, mock_user, mock_repo)

    mock_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_dicelog.id
    assert result.user_id == mock_user.id
    assert result.roll == sample_dicelog.roll
    assert result.result == sample_dicelog.result


def test_get_log_not_found(mock_request, mock_user, mock_repo):
    """Test get log raises HTTPException when log not found."""
    mock_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_log(mock_request, 999, mock_user, mock_repo)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Dice log not found."


def test_get_log_forbidden(mock_request, mock_other_user, mock_repo, sample_dicelog):
    """Test get log raises HTTPException when user is not owner."""
    mock_repo.get_by_id.return_value = sample_dicelog

    with pytest.raises(HTTPException) as exc_info:
        get_log(mock_request, 1, mock_other_user, mock_repo)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed."


def test_get_log_exception(mock_request, mock_user, mock_repo):
    """Test get log raises HTTPException on generic error."""
    mock_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc_info:
        get_log(mock_request, 1, mock_user, mock_repo)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error while fetching dice log."


def test_get_log_with_diceset(mock_request, mock_user, mock_repo):
    """Test get log with diceset_id."""
    log_with_diceset = DiceLogPublic(
        id=5,
        user_id=1,
        campaign_id=10,
        dnd_class_id=5,
        diceset_id=3,
        roll="Set: [4,5,6]",
        result=15,
        timestamp=datetime.now()
    )
    mock_repo.get_by_id.return_value = log_with_diceset

    result = get_log(mock_request, 5, mock_user, mock_repo)

    assert result.diceset_id == 3
    assert result.roll == "Set: [4,5,6]"
