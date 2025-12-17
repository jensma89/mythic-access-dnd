# """
# test_campaigns.py
# 
# Tests for campaign endpoints.
# """
# from fastapi.testclient import TestClient
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token
# from services.campaign.campaign_service import CampaignService
# from models.schemas.campaign_schema import CampaignCreate
# from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
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
#     """Create the authentication header."""
#     token = get_test_token(user)
#     return {"Authorization": f"Bearer {token}"}
# 
# 
# def get_campaign_service(session):
#     """Factory for CampaignService using test session."""
#     return CampaignService(
#         SqlAlchemyCampaignRepository(session),
#         SqlAlchemyClassRepository(session),
#         SqlAlchemyDiceSetRepository(session),
#         SqlAlchemyDiceLogRepository(session)
#     )
# 
# 
# def test_create_campaign():
#     """Test to create a new campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     client = TestClient(app)
# 
#     payload = {
#         "title": "Test Campaign",
#         "genre": "Fantasy",
#         "description": "A test campaign",
#         "max_classes": 4
#     }
# 
#     response = client.post(
#         "/campaigns/",
#         json=payload,
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["title"] == "Test Campaign"
#     assert data["genre"] == "Fantasy"
#     assert data["created_by"] == user.id
# 
# 
# def test_read_campaign_success():
#     """Test for reading a campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     # Create campaign first
#     payload = CampaignCreate(
#         title="My Campaign",
#         genre="SciFi",
#         description="Space adventure",
#         max_classes=3
#     )
#     payload.set_user(user.id)
#     campaign = service.create_campaign(payload)
# 
#     response = client.get(
#         f"/campaigns/{campaign.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == campaign.id
# 
# 
# def test_read_campaign_not_found():
#     """Test for retrieve non existing campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     client = TestClient(app)
# 
#     response = client.get(
#         "/campaigns/9999",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]
# 
# 
# def test_read_campaign_forbidden():
#     """Test to read a campaign from a another user."""
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     # Create campaign for owner
#     payload = CampaignCreate(
#         title="Owner's Campaign",
#         genre="Fantasy",
#         description="Private",
#         max_classes=2
#     )
#     payload.set_user(owner.id)
#     campaign = service.create_campaign(payload)
# 
#     # Other user tries to access
#     response = client.get(
#         f"/campaigns/{campaign.id}",
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
#     assert response.json()["detail"] == "Not allowed"
# 
# 
# def test_update_campaign_success():
#     """Test for updating campaign successfully."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     payload = CampaignCreate(
#         title="Campaign to Update",
#         genre="Fantasy",
#         description="Before update",
#         max_classes=2
#     )
#     payload.set_user(user.id)
#     campaign = service.create_campaign(payload)
# 
#     update_payload = {
#         "title": "Updated Campaign",
#         "description": "After update"
#     }
#     response = client.patch(
#         f"/campaigns/{campaign.id}",
#         json=update_payload,
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["title"] == "Updated Campaign"
# 
# 
# def test_update_campaign_forbidden():
#     """Test to update by unauthorized user."""
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     payload = CampaignCreate(
#         title="Owner Campaign",
#         genre="Fantasy",
#         description="Private",
#         max_classes=2
#     )
#     payload.set_user(owner.id)
#     campaign = service.create_campaign(payload)
# 
#     update_payload = {"title": "Hacked!"}
#     response = client.patch(
#         f"/campaigns/{campaign.id}",
#         json=update_payload,
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
# 
# 
# def test_delete_campaign_success():
#     """Test delete campaign successfully."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     payload = CampaignCreate(
#         title="To Delete",
#         genre="Fantasy",
#         description="Temp",
#         max_classes=1
#     )
#     payload.set_user(user.id)
#     campaign = service.create_campaign(payload)
# 
#     response = client.delete(
#         f"/campaigns/{campaign.id}",
#         headers=auth_header(user)
#     )
#     assert response.status_code == 200
#     assert response.json()["id"] == campaign.id
# 
# 
# def test_delete_campaign_forbidden():
#     """Test to delete campaign by unauthorized user."""
#     session = Session(test_engine)
#     owner = create_test_user(session)
#     other = create_test_user(session)
#     client = TestClient(app)
# 
#     service = get_campaign_service(session)
# 
#     payload = CampaignCreate(
#         title="Owner Campaign",
#         genre="Fantasy",
#         description="Private",
#         max_classes=2
#     )
#     payload.set_user(owner.id)
#     campaign = service.create_campaign(payload)
# 
#     response = client.delete(
#         f"/campaigns/{campaign.id}",
#         headers=auth_header(other)
#     )
#     assert response.status_code == 403
#


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from fastapi import HTTPException, Request
from routes.campaign.campaigns import (
    read_campaign,
    read_campaigns,
    create_campaign,
    update_campaign,
    delete_campaign
)
from models.schemas.campaign_schema import CampaignCreateInput, CampaignUpdate, CampaignPublic
from models.db_models.table_models import User
from services.campaign.campaign_service_exceptions import (
    CampaignNotFoundError,
    CampaignServiceError
)
from dependencies import CampaignQueryParams, Pagination
from datetime import datetime


@pytest.fixture
def mock_request():
    """Fixture for mocked request object."""
    return Mock(spec=Request)


@pytest.fixture
def mock_service():
    """Fixture for mocked campaign service."""
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
def sample_campaign():
    """Fixture for sample campaign."""
    return CampaignPublic(
        id=1,
        title="Test Campaign",
        genre="Fantasy",
        description="A test campaign",
        max_classes=4,
        user_id=1,
        created_by=1,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_campaign_create_input():
    """Fixture for sample campaign creation input."""
    return CampaignCreateInput(
        title="New Campaign",
        genre="Sci-Fi",
        description="A new campaign",
        max_classes=5
    )


@pytest.fixture
def mock_pagination():
    """Fixture for mocked pagination."""
    return Pagination(offset=0, limit=100)


@pytest.fixture
def mock_filters():
    """Fixture for mocked campaign query params."""
    return CampaignQueryParams()


# Tests for read_campaign function
def test_read_campaign_success(mock_request, mock_service, mock_user, sample_campaign):
    """Test successful campaign retrieval."""
    mock_service.get_campaign.return_value = sample_campaign

    result = read_campaign(mock_request, 1, mock_user, mock_service)

    mock_service.get_campaign.assert_called_once_with(1)
    assert result.id == sample_campaign.id
    assert result.title == sample_campaign.title


def test_read_campaign_not_found(mock_request, mock_service, mock_user):
    """Test read campaign raises HTTPException when campaign not found."""
    mock_service.get_campaign.side_effect = CampaignNotFoundError("Campaign not found")

    with pytest.raises(HTTPException) as exc_info:
        read_campaign(mock_request, 999, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Campaign not found."


def test_read_campaign_service_error(mock_request, mock_service, mock_user):
    """Test read campaign raises HTTPException on service error."""
    mock_service.get_campaign.side_effect = CampaignServiceError("Database error")

    with pytest.raises(HTTPException) as exc_info:
        read_campaign(mock_request, 1, mock_user, mock_service)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error while retrieving campaign."


def test_read_campaign_forbidden(mock_request, mock_service, mock_other_user, sample_campaign):
    """Test read campaign raises HTTPException when user is not owner."""
    mock_service.get_campaign.return_value = sample_campaign

    with pytest.raises(HTTPException) as exc_info:
        read_campaign(mock_request, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


# Tests for read_campaigns function
def test_read_campaigns_success(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test successful campaigns list retrieval."""
    campaigns = [
        CampaignPublic(id=1, title="Campaign 1", genre="Fantasy", description="Test 1", max_classes=4, user_id=1, created_by=1, created_at=datetime.now()),
        CampaignPublic(id=2, title="Campaign 2", genre="Sci-Fi", description="Test 2", max_classes=5, user_id=1, created_by=1, created_at=datetime.now())
    ]
    mock_service.list_campaigns.return_value = campaigns

    result = read_campaigns(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    mock_service.list_campaigns.assert_called_once_with(
        offset=0,
        limit=100,
        filters=mock_filters
    )
    assert len(result) == 2
    assert result[0].title == "Campaign 1"
    assert result[1].title == "Campaign 2"
    assert mock_filters.user_id == mock_user.id


def test_read_campaigns_empty_list(mock_request, mock_service, mock_user, mock_pagination, mock_filters):
    """Test campaigns list returns empty list."""
    mock_service.list_campaigns.return_value = []

    result = read_campaigns(mock_request, mock_user, mock_pagination, mock_filters, mock_service)

    assert isinstance(result, list)
    assert len(result) == 0
    assert mock_filters.user_id == mock_user.id


# Tests for create_campaign function
def test_create_campaign_success(mock_request, mock_service, mock_user, sample_campaign_create_input, sample_campaign):
    """Test successful campaign creation."""
    mock_service.create_campaign.return_value = sample_campaign

    result = create_campaign(mock_request, sample_campaign_create_input, mock_user, mock_service)

    mock_service.create_campaign.assert_called_once()
    assert result.id == sample_campaign.id
    assert result.title == sample_campaign.title
    assert result.created_by == mock_user.id


# Tests for update_campaign function
def test_update_campaign_success(mock_request, mock_service, mock_user, sample_campaign):
    """Test successful campaign update."""
    updated_campaign = CampaignPublic(
        id=1,
        title="Updated Campaign",
        genre="Fantasy",
        description="Updated description",
        max_classes=4,
        user_id=1,
        created_by=1,
        created_at=datetime.now()
    )
    mock_service.get_campaign.return_value = sample_campaign
    mock_service.update_campaign.return_value = updated_campaign

    update_data = CampaignUpdate(title="Updated Campaign", description="Updated description")
    result = update_campaign(mock_request, update_data, 1, mock_user, mock_service)

    mock_service.get_campaign.assert_called_once_with(1)
    mock_service.update_campaign.assert_called_once_with(1, update_data)
    assert result.title == "Updated Campaign"
    assert result.description == "Updated description"


def test_update_campaign_forbidden(mock_request, mock_service, mock_other_user, sample_campaign):
    """Test update campaign raises HTTPException when user is not owner."""
    mock_service.get_campaign.return_value = sample_campaign

    update_data = CampaignUpdate(title="Hacked")

    with pytest.raises(HTTPException) as exc_info:
        update_campaign(mock_request, update_data, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


def test_update_campaign_not_found(mock_request, mock_service, mock_user, sample_campaign):
    """Test update campaign raises HTTPException when update returns None."""
    mock_service.get_campaign.return_value = sample_campaign
    mock_service.update_campaign.return_value = None

    update_data = CampaignUpdate(title="New Title")

    with pytest.raises(HTTPException) as exc_info:
        update_campaign(mock_request, update_data, 1, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Campaign not found"


# Tests for delete_campaign function
def test_delete_campaign_success(mock_request, mock_service, mock_user, sample_campaign):
    """Test successful campaign deletion."""
    mock_service.get_campaign.return_value = sample_campaign
    mock_service.delete_campaign.return_value = sample_campaign

    result = delete_campaign(mock_request, 1, mock_user, mock_service)

    mock_service.get_campaign.assert_called_once_with(1)
    mock_service.delete_campaign.assert_called_once_with(1)
    assert result.id == sample_campaign.id


def test_delete_campaign_forbidden(mock_request, mock_service, mock_other_user, sample_campaign):
    """Test delete campaign raises HTTPException when user is not owner."""
    mock_service.get_campaign.return_value = sample_campaign

    with pytest.raises(HTTPException) as exc_info:
        delete_campaign(mock_request, 1, mock_other_user, mock_service)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Not allowed"


def test_delete_campaign_not_found(mock_request, mock_service, mock_user, sample_campaign):
    """Test delete campaign raises HTTPException when delete returns None."""
    mock_service.get_campaign.return_value = sample_campaign
    mock_service.delete_campaign.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        delete_campaign(mock_request, 1, mock_user, mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Campaign not found"
