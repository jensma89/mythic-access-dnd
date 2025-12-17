# """
# test_classes.py
# 
# Tests for dnd_class endpoints.
# """
# from fastapi.testclient import TestClient
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
# from services.dnd_class.class_service import ClassService
# from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassSkills
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
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
# def get_class_service(session):
#     """Factory to create ClassService with test session."""
#     return ClassService(
#         SqlAlchemyClassRepository(session),
#         SqlAlchemyDiceSetRepository(session),
#         SqlAlchemyDiceLogRepository(session)
#     )
# 
# 
# def test_create_class():
#     """Test creating a new dnd_class."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     # Create payload with required skills
#     payload = ClassCreate(
#         name="Testurion",
#         dnd_class="Warrior",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
# 
#     response = client.post(
#         "/classes/",
#         json=payload.model_dump(),
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Testurion"
#     assert data["user_id"] == user.id
# 
# 
# def test_read_class_success():
#     """Test reading a dnd_class successfully."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     service = get_class_service(session)
# 
#     payload = ClassCreate(
#         name="Fidus",
#         dnd_class="Mage",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
#     dnd_class = service.create_class(payload)
# 
#     response = client.get(
#         f"/classes/{dnd_class.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == dnd_class.id
# 
# 
# def test_read_class_not_found():
#     """Test reading a non-existing dnd_class returns 404."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     response = client.get(
#         "/classes/9999",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]
# 
# 
# def test_update_class_success():
#     """Test updating a dnd_class successfully."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     service = get_class_service(session)
# 
#     payload = ClassCreate(
#         name="Aldrion",
#         dnd_class="Rogue",
#         race="Elf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
#     dnd_class = service.create_class(payload)
# 
#     update_payload = ClassUpdate(
#         notes="Updated stealth master"
#     )
# 
#     response = client.patch(
#         f"/classes/{dnd_class.id}",
#         json=update_payload.model_dump(exclude_unset=True),
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["notes"] == "Updated stealth master"
# 
# 
# def test_update_class_forbidden():
#     """Test that updating a dnd_class
#     by another user is forbidden."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     campaign = create_test_campaign(session, owner)
#     service = get_class_service(session)
# 
#     payload = ClassCreate(
#         name="Hannes",
#         dnd_class="Paladin",
#         race="Human",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(owner.id)
#     dnd_class = service.create_class(payload)
# 
#     update_payload = ClassUpdate(notes="Hacked!")
# 
#     response = client.patch(
#         f"/classes/{dnd_class.id}",
#         json=update_payload.model_dump(exclude_unset=True),
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
# 
# 
# def test_delete_class_success():
#     """Test deleting a dnd_class successfully."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
#     service = get_class_service(session)
# 
#     payload = ClassCreate(
#         name="Schimli",
#         dnd_class="Ranger",
#         race="Dwarf",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(user.id)
#     dnd_class = service.create_class(payload)
# 
#     response = client.delete(
#         f"/classes/{dnd_class.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == dnd_class.id
# 
# 
# def test_delete_class_forbidden():
#     """Test that deleting a dnd_class
#     by another user is forbidden."""
#     client = TestClient(app)
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     campaign = create_test_campaign(session, owner)
#     service = get_class_service(session)
# 
#     payload = ClassCreate(
#         name="Songus",
#         dnd_class="Bard",
#         race="Halfling",
#         campaign_id=campaign.id,
#         skills=ClassSkills()
#     )
#     payload.set_user(owner.id)
#     dnd_class = service.create_class(payload)
# 
#     response = client.delete(
#         f"/classes/{dnd_class.id}",
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
#


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from fastapi import HTTPException, Request
from routes.dnd_class.dnd_classes import (
    read_class,
    read_classes,
    create_class,
    update_class,
    delete_class
)
from models.schemas.class_schema import ClassCreateInput, ClassUpdate, ClassPublic, ClassSkills
from models.db_models.table_models import User
from services.dnd_class.class_service_exceptions import ClassNotFoundError
from dependencies import ClassQueryParams, Pagination
from datetime import datetime


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_service():
    """Fixture for mocked class service."""
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
def sample_class():
    """Fixture for sample dnd class."""
    return ClassPublic(
        id=1,
        name="Test Warrior",
        dnd_class="Warrior",
        race="Human",
        user_id=1,
        campaign_id=10,
        skills=ClassSkills(),
        notes=None,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_class_create_input():
    """Fixture for sample class creation input."""
    return ClassCreateInput(
        name="New Mage",
        dnd_class="Mage",
        race="Elf",
        campaign_id=10,
        skills=ClassSkills()
    )


@pytest.fixture
def mock_pagination():
    """Fixture for mocked pagination."""
    return Pagination(offset=0, limit=100)


@pytest.fixture
def mock_filters():
    """Fixture for mocked class query params."""
    return ClassQueryParams()


# Tests for read_class function
def test_read_class_success(mock_request, mock_service, mock_user, sample_class):
    """Test successful class retrieval."""
    mock_service.get_class.return_value = sample_class

    result = read_class(mock_request, 1, mock_user, mock_service)

    mock_service.get_class.assert_called_once_with(1)
    assert result.id == sample_class.id
    assert result.name == sample_class.name


def test_read_class_not_found(mock_request, mock_service, mock_user):
    """Test read class raises HTTPException when class not found."""
    mock_service.get_class.side_effect = ClassNotFoundError("Class not found")

    with pytest.raises(HTTPException) as exc_info:
        read_class(mock_request, 999, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Class not found"


def test_read_class_forbidden(mock_request, mock_service, mock_other_user, sample_class):
    """Test read class raises HTTPException when user is not owner."""
    mock_service.get_class.return_value = sample_class

    with pytest.raises(HTTPException) as exc_info:
        read_class(mock_request, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


# Tests for read_classes function
def test_read_classes_success(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test successful classes list retrieval."""
    classes = [
        ClassPublic(id=1, name="Warrior 1", dnd_class="Warrior", race="Human", user_id=1, campaign_id=10, skills=ClassSkills(), notes=None, created_at=datetime.now()),
        ClassPublic(id=2, name="Mage 1", dnd_class="Mage", race="Elf", user_id=1, campaign_id=10, skills=ClassSkills(), notes=None, created_at=datetime.now())
    ]
    mock_service.list_classes.return_value = classes

    result = read_classes(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    mock_service.list_classes.assert_called_once_with(
        offset=0,
        limit=100,
        filters=mock_filters
    )
    assert len(result) == 2
    assert result[0].name == "Warrior 1"
    assert result[1].name == "Mage 1"


def test_read_classes_empty(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test classes list returns empty list."""
    mock_service.list_classes.return_value = []

    result = read_classes(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    assert isinstance(result, list)
    assert len(result) == 0


# Tests for create_class function
def test_create_class_success(mock_request, mock_service, mock_user, sample_class_create_input, sample_class):
    """Test successful class creation."""
    mock_service.create_class.return_value = sample_class

    result = create_class(mock_request, sample_class_create_input, mock_user, mock_service)

    mock_service.create_class.assert_called_once()
    assert result.id == sample_class.id
    assert result.name == sample_class.name


# Tests for update_class function
def test_update_class_success(mock_request, mock_service, mock_user, sample_class):
    """Test successful class update."""
    updated_class = ClassPublic(
        id=1,
        name="Test Warrior",
        dnd_class="Warrior",
        race="Human",
        user_id=1,
        campaign_id=10,
        skills=ClassSkills(),
        notes="Updated notes",
        created_at=datetime.now()
    )
    mock_service.get_class.return_value = sample_class
    mock_service.update_class.return_value = updated_class

    update_data = ClassUpdate(notes="Updated notes")
    result = update_class(mock_request, update_data, 1, mock_user, mock_service)

    mock_service.get_class.assert_called_once_with(1)
    mock_service.update_class.assert_called_once_with(1, update_data)
    assert result.notes == "Updated notes"


def test_update_class_forbidden(mock_request, mock_service, mock_other_user, sample_class):
    """Test update class raises HTTPException when user is not owner."""
    mock_service.get_class.return_value = sample_class

    update_data = ClassUpdate(notes="Hacked")

    with pytest.raises(HTTPException) as exc_info:
        update_class(mock_request, update_data, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


def test_update_class_not_found(mock_request, mock_service, mock_user, sample_class):
    """Test update class raises HTTPException when update returns None."""
    mock_service.get_class.return_value = sample_class
    mock_service.update_class.return_value = None

    update_data = ClassUpdate(notes="New notes")

    with pytest.raises(HTTPException) as exc_info:
        update_class(mock_request, update_data, 1, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Class not found."


# Tests for delete_class function
def test_delete_class_success(mock_request, mock_service, mock_user, sample_class):
    """Test successful class deletion."""
    mock_service.get_class.return_value = sample_class
    mock_service.delete_class.return_value = sample_class

    result = delete_class(mock_request, 1, mock_user, mock_service)

    mock_service.get_class.assert_called_once_with(1)
    mock_service.delete_class.assert_called_once_with(1)
    assert result.id == sample_class.id


def test_delete_class_forbidden(mock_request, mock_service, mock_other_user, sample_class):
    """Test delete class raises HTTPException when user is not owner."""
    mock_service.get_class.return_value = sample_class

    with pytest.raises(HTTPException) as exc_info:
        delete_class(mock_request, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


def test_delete_class_not_found(mock_request, mock_service, mock_user):
    """Test delete class raises HTTPException when class not found."""
    mock_service.get_class.side_effect = ClassNotFoundError("Class not found")

    with pytest.raises(HTTPException) as exc_info:
        delete_class(mock_request, 999, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Class not found"
