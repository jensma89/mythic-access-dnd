# """
# test_dices.py
# 
# Tests for dice endpoints.
# """
# from fastapi.testclient import TestClient
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
# from services.dice.dice_service import DiceService
# from models.schemas.dice_schema import DiceCreate
# from models.schemas.class_schema import ClassCreate, ClassSkills
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
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
# def get_dice_service(session):
#     """Factory to create DiceService with test session."""
#     return DiceService(
#         SqlAlchemyDiceRepository(session),
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
#     payload = DiceCreate(
#         name=name,
#         sides=sides
#     )
#     return service.create_dice(payload)
# 
# 
# def test_read_dice_success():
#     """Test reading a dice successfully."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     # Create a test dice
#     dice = create_test_dice(session, "D20", 20)
# 
#     response = client.get(
#         f"/dices/{dice.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == dice.id
#     assert data["sides"] == 20
#     assert data["name"] == "D20"
# 
# 
# def test_read_dice_not_found():
#     """Test reading a non-existing dice returns 404."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         "/dices/99999",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 404
#     detail = response.json()["detail"]
#     assert (
#             "not found" in detail.lower()
#             or "dice" in detail.lower())
# 
# 
# def test_read_dices_list():
#     """Test listing all dices."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     # Create some test dices
#     create_test_dice(session, "D4", 4)
#     create_test_dice(session, "D8", 8)
# 
#     response = client.get(
#         "/dices/",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) >= 2
# 
# 
# def test_roll_dice_success():
#     """Test rolling a dice successfully."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     # Create a test dice
#     dice = create_test_dice(session, "D6", 6)
# 
#     response = client.post(
#         f"/dices/{dice.id}/roll",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "result" in data
#     assert "id" in data
#     assert data["id"] == dice.id
#     assert isinstance(data["result"], int)
#     assert 1 <= data["result"] <= 6
# 
# 
# def test_roll_dice_not_found():
#     """Test rolling a non-existing dice returns 404."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.post(
#         "/dices/99999/roll",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"].lower()
# 
# 
# def test_roll_dice_with_campaign():
#     """Test rolling a dice with campaign_id parameter."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create a test dice
#     dice = create_test_dice(session, "D12", 12)
# 
#     response = client.post(
#         f"/dices/{dice.id}/roll?campaign_id={campaign.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "result" in data
#     assert isinstance(data["result"], int)
#     assert 1 <= data["result"] <= 12
# 
# 
# def test_roll_dice_with_class():
#     """Test rolling a dice with class_id parameter."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create a class
#     class_service = get_class_service(session)
#     payload = ClassCreate(
#         name="Testchar",
#         dnd_class="Fighter",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
#     dnd_class = class_service.create_class(payload)
# 
#     # Create a test dice
#     dice = create_test_dice(session, "D10", 10)
# 
#     response = client.post(
#         f"/dices/{dice.id}/roll?class_id={dnd_class.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "result" in data
#     assert isinstance(data["result"], int)
#     assert 1 <= data["result"] <= 10
# 
# 
# def test_roll_dice_with_campaign_and_class():
#     """Test rolling a dice with both campaign_id and class_id."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create a class
#     class_service = get_class_service(session)
#     payload = ClassCreate(
#         name="Testchar2",
#         dnd_class="Wizard",
#         race="Elf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
#     dnd_class = class_service.create_class(payload)
# 
#     # Create a test dice
#     dice = create_test_dice(session, "D100", 100)
# 
#     response = client.post(
#         f"/dices/{dice.id}/roll?campaign_id={campaign.id}&class_id={dnd_class.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "result" in data
#     assert isinstance(data["result"], int)
#     assert 1 <= data["result"] <= 100
# 
# 
# def test_read_dices_pagination():
#     """Test pagination for dice list."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     # Create multiple test dices
#     for i in range(10):
#         create_test_dice(session, f"D{i+4}", i+4)
# 
#     response = client.get(
#         "/dices/?offset=0&limit=5",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert len(data) <= 5
# 
# 
# def test_roll_dice_multiple_times():
#     """Test rolling the same dice multiple times
#     produces different results."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     # Create a test dice with many sides
#     dice = create_test_dice(session, "D20", 20)
# 
#     results = []
#     for _ in range(10):
#         response = client.post(
#             f"/dices/{dice.id}/roll",
#             headers=auth_header(user)
#         )
#         assert response.status_code == 200
#         results.append(response.json()["result"])
# 
#     # Check all results are valid
#     assert all(1 <= r <= 20 for r in results)
#     # Check we got at least some variation (not all same)
#     assert len(set(results)) > 1
#


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from fastapi import HTTPException, Request
from routes.dice.dices import read_dice, read_dices, roll_dice
from models.schemas.dice_schema import DicePublic, DiceRollResult
from models.db_models.table_models import User
from services.dice.dice_service_exceptions import DiceNotFoundError
from dependencies import Pagination
from datetime import datetime


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_service():
    """Fixture for mocked dice service."""
    service = Mock()
    service.repo = Mock()
    return service


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
def sample_dice():
    """Fixture for sample dice."""
    return DicePublic(
        id=1,
        name="D20",
        sides=20,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_dice_roll_result():
    """Fixture for sample dice roll result."""
    return DiceRollResult(
        id=1,
        name="D20",
        sides=20,
        result=15
    )


@pytest.fixture
def mock_pagination():
    """Fixture for mocked pagination."""
    return Pagination(offset=0, limit=100)


# Tests for read_dice function
def test_read_dice_success(mock_request, mock_service, mock_user, sample_dice):
    """Test successful dice retrieval."""
    mock_service.get_dice.return_value = sample_dice

    result = read_dice(mock_request, 1, mock_user, mock_service)

    mock_service.get_dice.assert_called_once_with(1)
    assert result.id == sample_dice.id
    assert result.name == sample_dice.name
    assert result.sides == sample_dice.sides


def test_read_dice_not_found(mock_request, mock_service, mock_user):
    """Test read dice raises HTTPException when dice not found."""
    mock_service.get_dice.side_effect = DiceNotFoundError("Dice not found")

    with pytest.raises(HTTPException) as exc_info:
        read_dice(mock_request, 999, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Dice not found"


# Tests for read_dices function
def test_read_dices_success(mock_request, mock_service, mock_user, mock_pagination):
    """Test successful dice list retrieval."""
    dices = [
        DicePublic(id=1, name="D4", sides=4, created_at=datetime.now()),
        DicePublic(id=2, name="D6", sides=6, created_at=datetime.now()),
        DicePublic(id=3, name="D20", sides=20, created_at=datetime.now())
    ]
    mock_service.list_dices.return_value = dices

    result = read_dices(mock_request, mock_user, mock_pagination, mock_service)

    mock_service.list_dices.assert_called_once_with(offset=0, limit=100)
    assert len(result) == 3
    assert result[0].name == "D4"
    assert result[1].name == "D6"
    assert result[2].name == "D20"


def test_read_dices_empty_list(mock_request, mock_service, mock_user, mock_pagination):
    """Test dice list returns empty list."""
    mock_service.list_dices.return_value = []

    result = read_dices(mock_request, mock_user, mock_pagination, mock_service)

    assert isinstance(result, list)
    assert len(result) == 0


# Tests for roll_dice function
def test_roll_dice_success(mock_request, mock_service, mock_user, sample_dice, sample_dice_roll_result):
    """Test successful dice roll."""
    mock_service.repo.get_by_id.return_value = sample_dice
    mock_service.roll_dice.return_value = sample_dice_roll_result

    result = roll_dice(mock_request, 1, None, None, mock_user, mock_service)

    mock_service.repo.get_by_id.assert_called_once_with(1)
    mock_service.roll_dice.assert_called_once_with(
        dice_id=1,
        user_id=mock_user.id,
        campaign_id=None,
        dnd_class_id=None
    )
    assert result.id == sample_dice_roll_result.id
    assert result.result == sample_dice_roll_result.result
    assert result.sides == sample_dice_roll_result.sides


def test_roll_dice_with_campaign_id(mock_request, mock_service, mock_user, sample_dice, sample_dice_roll_result):
    """Test dice roll with campaign_id parameter."""
    mock_service.repo.get_by_id.return_value = sample_dice
    mock_service.roll_dice.return_value = sample_dice_roll_result

    result = roll_dice(mock_request, 1, 10, None, mock_user, mock_service)

    mock_service.roll_dice.assert_called_once_with(
        dice_id=1,
        user_id=mock_user.id,
        campaign_id=10,
        dnd_class_id=None
    )
    assert result.result == sample_dice_roll_result.result


def test_roll_dice_with_class_id(mock_request, mock_service, mock_user, sample_dice, sample_dice_roll_result):
    """Test dice roll with dnd_class_id parameter."""
    mock_service.repo.get_by_id.return_value = sample_dice
    mock_service.roll_dice.return_value = sample_dice_roll_result

    result = roll_dice(mock_request, 1, None, 5, mock_user, mock_service)

    mock_service.roll_dice.assert_called_once_with(
        dice_id=1,
        user_id=mock_user.id,
        campaign_id=None,
        dnd_class_id=5
    )
    assert result.result == sample_dice_roll_result.result


def test_roll_dice_with_campaign_and_class(mock_request, mock_service, mock_user, sample_dice, sample_dice_roll_result):
    """Test dice roll with both campaign_id and dnd_class_id."""
    mock_service.repo.get_by_id.return_value = sample_dice
    mock_service.roll_dice.return_value = sample_dice_roll_result

    result = roll_dice(mock_request, 1, 10, 5, mock_user, mock_service)

    mock_service.roll_dice.assert_called_once_with(
        dice_id=1,
        user_id=mock_user.id,
        campaign_id=10,
        dnd_class_id=5
    )
    assert result.result == sample_dice_roll_result.result


def test_roll_dice_not_found(mock_request, mock_service, mock_user):
    """Test roll dice raises HTTPException when dice not found."""
    mock_service.repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        roll_dice(mock_request, 999, None, None, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Dice not found"


def test_roll_dice_roll_result_none(mock_request, mock_service, mock_user, sample_dice):
    """Test roll dice raises HTTPException when roll_result is None."""
    mock_service.repo.get_by_id.return_value = sample_dice
    mock_service.roll_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        roll_dice(mock_request, 1, None, None, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Dice not found."
