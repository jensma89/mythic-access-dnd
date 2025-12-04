"""
test_campaigns.py

Tests for campaign endpoints.
"""
from fastapi.testclient import TestClient

from main import app
from dependencies import get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token
from services.campaign.campaign_service import CampaignService
from models.schemas.campaign_schema import CampaignCreate
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository


# Override DB dependency
app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


def auth_header(user):
    """Create the authentication header."""
    token = get_test_token(user)
    return {"Authorization": f"Bearer {token}"}


def get_campaign_service(session):
    """Factory for CampaignService using test session."""
    return CampaignService(
        SqlAlchemyCampaignRepository(session),
        SqlAlchemyClassRepository(session),
        SqlAlchemyDiceSetRepository(session),
        SqlAlchemyDiceLogRepository(session)
    )


def test_create_campaign():
    """Test to create a new campaign."""
    session = next(get_test_session())
    user = create_test_user(session)

    payload = {
        "title": "Test Campaign",
        "genre": "Fantasy",
        "description": "A test campaign",
        "max_classes": 4
    }

    response = client.post(
        "/campaigns/",
        json=payload,
        headers=auth_header(user)
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Campaign"
    assert data["genre"] == "Fantasy"
    assert data["created_by"] == user.id


def test_read_campaign_success():
    """Test for reading a campaign."""
    session = next(get_test_session())
    user = create_test_user(session)

    service = get_campaign_service(session)

    # Create campaign first
    payload = CampaignCreate(
        title="My Campaign",
        genre="SciFi",
        description="Space adventure",
        max_classes=3
    )
    payload.set_user(user.id)
    campaign = service.create_campaign(payload)

    response = client.get(
        f"/campaigns/{campaign.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["id"] == campaign.id


def test_read_campaign_not_found():
    """Test for retrieve non existing campaign."""
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.get(
        "/campaigns/9999",
        headers=auth_header(user)
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_read_campaign_forbidden():
    """Test to read a campaign from a another user."""
    session = next(get_test_session())
    owner = create_test_user(session)
    other = create_test_user(session)

    service = get_campaign_service(session)

    # Create campaign for owner
    payload = CampaignCreate(
        title="Owner's Campaign",
        genre="Fantasy",
        description="Private",
        max_classes=2
    )
    payload.set_user(owner.id)
    campaign = service.create_campaign(payload)

    # Other user tries to access
    response = client.get(
        f"/campaigns/{campaign.id}",
        headers=auth_header(other)
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not allowed"


def test_update_campaign_success():
    """Test for updating campaign successfully."""
    session = next(get_test_session())
    user = create_test_user(session)

    service = get_campaign_service(session)

    payload = CampaignCreate(
        title="Campaign to Update",
        genre="Fantasy",
        description="Before update",
        max_classes=2
    )
    payload.set_user(user.id)
    campaign = service.create_campaign(payload)

    update_payload = {
        "title": "Updated Campaign",
        "description": "After update"
    }
    response = client.patch(
        f"/campaigns/{campaign.id}",
        json=update_payload,
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Campaign"


def test_update_campaign_forbidden():
    """Test to update by unauthorized user."""
    session = next(get_test_session())
    owner = create_test_user(session)
    other = create_test_user(session)

    service = get_campaign_service(session)

    payload = CampaignCreate(
        title="Owner Campaign",
        genre="Fantasy",
        description="Private",
        max_classes=2
    )
    payload.set_user(owner.id)
    campaign = service.create_campaign(payload)

    update_payload = {"title": "Hacked!"}
    response = client.patch(
        f"/campaigns/{campaign.id}",
        json=update_payload,
        headers=auth_header(other)
    )
    assert response.status_code == 403


def test_delete_campaign_success():
    """Test delete campaign successfully."""
    session = next(get_test_session())
    user = create_test_user(session)

    service = get_campaign_service(session)

    payload = CampaignCreate(
        title="To Delete",
        genre="Fantasy",
        description="Temp",
        max_classes=1
    )
    payload.set_user(user.id)
    campaign = service.create_campaign(payload)

    response = client.delete(
        f"/campaigns/{campaign.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["id"] == campaign.id


def test_delete_campaign_forbidden():
    """Test to delete campaign by unauthorized user."""
    session = next(get_test_session())
    owner = create_test_user(session)
    other = create_test_user(session)

    service = get_campaign_service(session)

    payload = CampaignCreate(
        title="Owner Campaign",
        genre="Fantasy",
        description="Private",
        max_classes=2
    )
    payload.set_user(owner.id)
    campaign = service.create_campaign(payload)

    response = client.delete(
        f"/campaigns/{campaign.id}",
        headers=auth_header(other)
    )
    assert response.status_code == 403
