"""
test_campaign_service.py

Test for campaign service - business logic.
"""
import pytest
import uuid

from services.campaign.campaign_service import CampaignService
from services.campaign.campaign_service_exceptions import (
    CampaignNotFoundError,
    CampaignCreateError,
    CampaignUpdateError,
    CampaignDeleteError,
    CampaignServiceError
)
from models.schemas.campaign_schema import CampaignCreate, CampaignUpdate
from models.db_models.test_db import get_session as get_test_session
from models.db_models.test_db import test_engine
from sqlmodel import Session
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from dependencies import CampaignQueryParams
from auth.test_helpers import create_test_user



def test_create_campaign():
    """Test to create a new campaign."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    campaign_data = CampaignCreate(
        title="Test Campaign",
        genre="Fantasy",
        description="A test campaign",
        max_classes=4
    )
    campaign_data.set_user(user.id)

    campaign = service.create_campaign(campaign_data)

    assert campaign.title == "Test Campaign"
    assert campaign.genre == "Fantasy"
    assert campaign.id is not None


def test_get_campaign():
    """Test to get a campaign by ID."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    campaign_data = CampaignCreate(
        title="Get Test Campaign",
        genre="Sci-Fi",
        description="Test",
        max_classes=5
    )
    campaign_data.set_user(user.id)
    created = service.create_campaign(campaign_data)

    result = service.get_campaign(created.id)

    assert result.id == created.id
    assert result.title == "Get Test Campaign"


def test_get_campaign_not_found():
    """Test get campaign with non-existent ID."""
    session = Session(test_engine)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    with pytest.raises(CampaignNotFoundError):
        service.get_campaign(99999)


def test_list_campaigns():
    """Test to list all campaigns."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    campaign1_data = CampaignCreate(
        title="List Campaign 1",
        genre="Fantasy",
        description="Test 1",
        max_classes=3
    )
    campaign1_data.set_user(user.id)
    service.create_campaign(campaign1_data)

    campaign2_data = CampaignCreate(
        title="List Campaign 2",
        genre="Horror",
        description="Test 2",
        max_classes=4
    )
    campaign2_data.set_user(user.id)
    service.create_campaign(campaign2_data)

    filters = CampaignQueryParams(user_id=user.id)
    campaigns = service.list_campaigns(filters)

    assert isinstance(campaigns, list)


def test_list_campaigns_with_filter():
    """Test list campaigns with name filter."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    campaign_data = CampaignCreate(
        title=f"filtered_campaign_{suffix}",
        genre="Mystery",
        description="Filtered test",
        max_classes=3
    )
    campaign_data.set_user(user.id)
    service.create_campaign(campaign_data)

    filters = CampaignQueryParams(user_id=user.id, name=f"filtered_campaign_{suffix}")
    campaigns = service.list_campaigns(filters)

    assert len(campaigns) >= 1
    assert any(f"filtered_campaign_{suffix}" in c.title for c in campaigns)


def test_update_campaign():
    """Test to update a campaign."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    campaign_data = CampaignCreate(
        title=f"update_test_{suffix}",
        genre="Fantasy",
        description="Original",
        max_classes=4
    )
    campaign_data.set_user(user.id)
    campaign = service.create_campaign(campaign_data)

    new_suffix = uuid.uuid4().hex[:8]
    update_data = CampaignUpdate(title=f"updated_title_{new_suffix}")
    updated = service.update_campaign(campaign.id, update_data)

    assert updated is not None
    assert updated.id == campaign.id


def test_update_campaign_not_found():
    """Test update with non-existent campaign ID."""
    session = Session(test_engine)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    update_data = CampaignUpdate(title="new_title")

    with pytest.raises((CampaignNotFoundError, CampaignServiceError)):
        service.update_campaign(99999, update_data)


def test_delete_campaign():
    """Test to delete a campaign."""
    session = Session(test_engine)
    user = create_test_user(session)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    campaign_data = CampaignCreate(
        title="Delete Test Campaign",
        genre="Adventure",
        description="To be deleted",
        max_classes=3
    )
    campaign_data.set_user(user.id)
    campaign = service.create_campaign(campaign_data)

    deleted = service.delete_campaign(campaign.id)

    assert deleted is not None

    # Verify campaign is gone
    with pytest.raises(CampaignNotFoundError):
        service.get_campaign(campaign.id)


def test_delete_campaign_not_found():
    """Test delete with non-existent campaign ID."""
    session = Session(test_engine)
    service = CampaignService(
        campaign_repo=SqlAlchemyCampaignRepository(session),
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    with pytest.raises((CampaignNotFoundError, CampaignDeleteError, CampaignServiceError)):
        service.delete_campaign(99999)
