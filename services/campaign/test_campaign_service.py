# """
# test_campaign_service.py
# 
# Test for campaign service - business logic.
# """
# import pytest
# import uuid
# 
# from services.campaign.campaign_service import CampaignService
# from services.campaign.campaign_service_exceptions import (
#     CampaignNotFoundError,
#     CampaignCreateError,
#     CampaignUpdateError,
#     CampaignDeleteError,
#     CampaignServiceError
# )
# from models.schemas.campaign_schema import CampaignCreate, CampaignUpdate
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from dependencies import CampaignQueryParams
# from auth.test_helpers import create_test_user
# 
# 
# 
# def test_create_campaign():
#     """Test to create a new campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     campaign_data = CampaignCreate(
#         title="Test Campaign",
#         genre="Fantasy",
#         description="A test campaign",
#         max_classes=4
#     )
#     campaign_data.set_user(user.id)
# 
#     campaign = service.create_campaign(campaign_data)
# 
#     assert campaign.title == "Test Campaign"
#     assert campaign.genre == "Fantasy"
#     assert campaign.id is not None
# 
# 
# def test_get_campaign():
#     """Test to get a campaign by ID."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     campaign_data = CampaignCreate(
#         title="Get Test Campaign",
#         genre="Sci-Fi",
#         description="Test",
#         max_classes=5
#     )
#     campaign_data.set_user(user.id)
#     created = service.create_campaign(campaign_data)
# 
#     result = service.get_campaign(created.id)
# 
#     assert result.id == created.id
#     assert result.title == "Get Test Campaign"
# 
# 
# def test_get_campaign_not_found():
#     """Test get campaign with non-existent ID."""
#     session = Session(test_engine)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(CampaignNotFoundError):
#         service.get_campaign(99999)
# 
# 
# def test_list_campaigns():
#     """Test to list all campaigns."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     campaign1_data = CampaignCreate(
#         title="List Campaign 1",
#         genre="Fantasy",
#         description="Test 1",
#         max_classes=3
#     )
#     campaign1_data.set_user(user.id)
#     service.create_campaign(campaign1_data)
# 
#     campaign2_data = CampaignCreate(
#         title="List Campaign 2",
#         genre="Horror",
#         description="Test 2",
#         max_classes=4
#     )
#     campaign2_data.set_user(user.id)
#     service.create_campaign(campaign2_data)
# 
#     filters = CampaignQueryParams(user_id=user.id)
#     campaigns = service.list_campaigns(filters)
# 
#     assert isinstance(campaigns, list)
# 
# 
# def test_list_campaigns_with_filter():
#     """Test list campaigns with name filter."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     campaign_data = CampaignCreate(
#         title=f"filtered_campaign_{suffix}",
#         genre="Mystery",
#         description="Filtered test",
#         max_classes=3
#     )
#     campaign_data.set_user(user.id)
#     service.create_campaign(campaign_data)
# 
#     filters = CampaignQueryParams(user_id=user.id, name=f"filtered_campaign_{suffix}")
#     campaigns = service.list_campaigns(filters)
# 
#     assert len(campaigns) >= 1
#     assert any(f"filtered_campaign_{suffix}" in c.title for c in campaigns)
# 
# 
# def test_update_campaign():
#     """Test to update a campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     campaign_data = CampaignCreate(
#         title=f"update_test_{suffix}",
#         genre="Fantasy",
#         description="Original",
#         max_classes=4
#     )
#     campaign_data.set_user(user.id)
#     campaign = service.create_campaign(campaign_data)
# 
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = CampaignUpdate(title=f"updated_title_{new_suffix}")
#     updated = service.update_campaign(campaign.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == campaign.id
# 
# 
# def test_update_campaign_not_found():
#     """Test update with non-existent campaign ID."""
#     session = Session(test_engine)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = CampaignUpdate(title="new_title")
# 
#     with pytest.raises((CampaignNotFoundError, CampaignServiceError)):
#         service.update_campaign(99999, update_data)
# 
# 
# def test_delete_campaign():
#     """Test to delete a campaign."""
#     session = Session(test_engine)
#     user = create_test_user(session)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     campaign_data = CampaignCreate(
#         title="Delete Test Campaign",
#         genre="Adventure",
#         description="To be deleted",
#         max_classes=3
#     )
#     campaign_data.set_user(user.id)
#     campaign = service.create_campaign(campaign_data)
# 
#     deleted = service.delete_campaign(campaign.id)
# 
#     assert deleted is not None
# 
#     # Verify campaign is gone
#     with pytest.raises(CampaignNotFoundError):
#         service.get_campaign(campaign.id)
# 
# 
# def test_delete_campaign_not_found():
#     """Test delete with non-existent campaign ID."""
#     session = Session(test_engine)
#     service = CampaignService(
#         campaign_repo=SqlAlchemyCampaignRepository(session),
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((CampaignNotFoundError, CampaignDeleteError, CampaignServiceError)):
#         service.delete_campaign(99999)


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock, MagicMock
from services.campaign.campaign_service import CampaignService
from services.campaign.campaign_service_exceptions import (
    CampaignServiceError,
    CampaignNotFoundError,
    CampaignCreateError,
    CampaignUpdateError,
    CampaignDeleteError
)
from models.schemas.campaign_schema import CampaignCreate, CampaignUpdate, CampaignPublic
from dependencies import CampaignQueryParams


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
def campaign_service(mock_campaign_repo, mock_class_repo, mock_diceset_repo, mock_dicelog_repo):
    """Fixture for CampaignService instance with mocked repositories."""
    return CampaignService(
        campaign_repo=mock_campaign_repo,
        class_repo=mock_class_repo,
        diceset_repo=mock_diceset_repo,
        dicelog_repo=mock_dicelog_repo
    )


@pytest.fixture
def sample_campaign_data():
    """Fixture for sample campaign creation data."""
    campaign_data = CampaignCreate(
        title="Test Campaign",
        genre="Fantasy",
        description="A test campaign",
        max_classes=4
    )
    campaign_data.set_user(1)
    return campaign_data


@pytest.fixture
def sample_campaign():
    """Fixture for sample campaign."""
    from datetime import datetime
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


# Tests for create_campaign function
def test_create_campaign_success(campaign_service, mock_campaign_repo, sample_campaign_data, sample_campaign):
    """Test successful campaign creation."""
    mock_campaign_repo.add.return_value = sample_campaign

    result = campaign_service.create_campaign(sample_campaign_data)

    mock_campaign_repo.add.assert_called_once_with(sample_campaign_data)
    assert result.id == sample_campaign.id
    assert result.title == sample_campaign.title
    assert result.genre == sample_campaign.genre


def test_create_campaign_repository_returns_none(campaign_service, mock_campaign_repo, sample_campaign_data):
    """Test campaign creation fails when repository returns None."""
    mock_campaign_repo.add.return_value = None

    with pytest.raises(CampaignCreateError) as exc_info:
        campaign_service.create_campaign(sample_campaign_data)

    assert "creating campaign" in str(exc_info.value)


def test_create_campaign_exception(campaign_service, mock_campaign_repo, sample_campaign_data):
    """Test campaign creation handles exceptions."""
    mock_campaign_repo.add.side_effect = Exception("Database error")

    with pytest.raises(CampaignCreateError) as exc_info:
        campaign_service.create_campaign(sample_campaign_data)

    assert "Error while creating campaign" in str(exc_info.value)


# Tests for get_campaign function
def test_get_campaign_success(campaign_service, mock_campaign_repo, sample_campaign):
    """Test successful campaign retrieval."""
    mock_campaign_repo.get_by_id.return_value = sample_campaign

    result = campaign_service.get_campaign(1)

    mock_campaign_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_campaign.id
    assert result.title == sample_campaign.title


def test_get_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test get campaign raises error when campaign not found."""
    mock_campaign_repo.get_by_id.return_value = None

    with pytest.raises(CampaignNotFoundError) as exc_info:
        campaign_service.get_campaign(999)

    assert "Campaign with ID 999 not found" in str(exc_info.value)


def test_get_campaign_exception(campaign_service, mock_campaign_repo):
    """Test get campaign handles exceptions."""
    mock_campaign_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(CampaignServiceError) as exc_info:
        campaign_service.get_campaign(1)

    assert "Error while retrieving campaign" in str(exc_info.value)


# Tests for list_campaigns function
def test_list_campaigns_success(campaign_service, mock_campaign_repo):
    """Test successful campaign listing."""
    from datetime import datetime
    now = datetime.now()
    campaigns = [
        CampaignPublic(id=1, title="Campaign 1", genre="Fantasy", description="Test 1", max_classes=4, user_id=1, created_by=1, created_at=now),
        CampaignPublic(id=2, title="Campaign 2", genre="Sci-Fi", description="Test 2", max_classes=5, user_id=1, created_by=1, created_at=now)
    ]
    mock_campaign_repo.list_all.return_value = campaigns

    filters = CampaignQueryParams(user_id=1)
    result = campaign_service.list_campaigns(filters, offset=0, limit=100)

    mock_campaign_repo.list_all.assert_called_once()
    assert len(result) == 2
    assert result[0].title == "Campaign 1"
    assert result[1].title == "Campaign 2"


def test_list_campaigns_with_filters(campaign_service, mock_campaign_repo):
    """Test campaign listing with name filter."""
    from datetime import datetime
    campaigns = [
        CampaignPublic(id=1, title="Filtered Campaign", genre="Fantasy", description="Test", max_classes=4, user_id=1, created_by=1, created_at=datetime.now())
    ]
    mock_campaign_repo.list_all.return_value = campaigns

    filters = CampaignQueryParams(user_id=1, name="Filtered")
    result = campaign_service.list_campaigns(filters, offset=5, limit=20)

    mock_campaign_repo.list_all.assert_called_once()
    assert len(result) == 1
    assert result[0].title == "Filtered Campaign"


def test_list_campaigns_empty(campaign_service, mock_campaign_repo):
    """Test campaign listing returns empty list."""
    mock_campaign_repo.list_all.return_value = []

    filters = CampaignQueryParams(user_id=1)
    result = campaign_service.list_campaigns(filters)

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_campaigns_exception(campaign_service, mock_campaign_repo):
    """Test list campaigns handles exceptions."""
    mock_campaign_repo.list_all.side_effect = Exception("Database error")

    filters = CampaignQueryParams(user_id=1)

    with pytest.raises(CampaignServiceError) as exc_info:
        campaign_service.list_campaigns(filters)

    assert "Error while listing campaigns" in str(exc_info.value)


# Tests for update_campaign function
def test_update_campaign_success(campaign_service, mock_campaign_repo):
    """Test successful campaign update."""
    from datetime import datetime
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
    mock_campaign_repo.update.return_value = updated_campaign

    update_data = CampaignUpdate(title="Updated Campaign", description="Updated description")
    result = campaign_service.update_campaign(1, update_data)

    mock_campaign_repo.update.assert_called_once_with(1, update_data)
    assert result.id == 1
    assert result.title == "Updated Campaign"
    assert result.description == "Updated description"


def test_update_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test update campaign raises error when campaign not found."""
    mock_campaign_repo.update.return_value = None

    update_data = CampaignUpdate(title="New Title")

    with pytest.raises((CampaignNotFoundError, CampaignServiceError)):
        campaign_service.update_campaign(999, update_data)


def test_update_campaign_exception(campaign_service, mock_campaign_repo):
    """Test update campaign handles exceptions."""
    mock_campaign_repo.update.side_effect = Exception("Database error")

    update_data = CampaignUpdate(title="New Title")

    with pytest.raises(CampaignServiceError) as exc_info:
        campaign_service.update_campaign(1, update_data)

    assert "Error while updating campaign" in str(exc_info.value)


# Tests for delete_campaign function
def test_delete_campaign_success(campaign_service, mock_campaign_repo, mock_class_repo,
                                 mock_diceset_repo, mock_dicelog_repo, sample_campaign):
    """Test successful campaign deletion with related entities."""
    # Setup mocks
    mock_campaign_repo.get_by_id.return_value = sample_campaign
    mock_dicelog_repo.list_by_campaign.return_value = [Mock(id=1), Mock(id=2)]
    mock_diceset_repo.list_by_campaign.return_value = [Mock(id=10), Mock(id=11)]
    mock_class_repo.list_by_campaign.return_value = [Mock(id=20)]
    mock_campaign_repo.delete.return_value = sample_campaign

    result = campaign_service.delete_campaign(1)

    # Verify deletion order: dice logs, dice sets, classes, campaign
    assert mock_dicelog_repo.delete.call_count == 2
    assert mock_diceset_repo.delete.call_count == 2
    assert mock_class_repo.delete.call_count == 1
    mock_campaign_repo.delete.assert_called_once_with(1)
    assert result == sample_campaign


def test_delete_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test delete campaign raises error when campaign not found."""
    mock_campaign_repo.get_by_id.return_value = None

    with pytest.raises(CampaignNotFoundError) as exc_info:
        campaign_service.delete_campaign(999)

    assert "Campaign with ID 999 not found" in str(exc_info.value)


def test_delete_campaign_deletion_fails(campaign_service, mock_campaign_repo, mock_class_repo,
                                       mock_diceset_repo, mock_dicelog_repo, sample_campaign):
    """Test delete campaign when final deletion returns None."""
    mock_campaign_repo.get_by_id.return_value = sample_campaign
    mock_dicelog_repo.list_by_campaign.return_value = []
    mock_diceset_repo.list_by_campaign.return_value = []
    mock_class_repo.list_by_campaign.return_value = []
    mock_campaign_repo.delete.return_value = None

    with pytest.raises(CampaignDeleteError) as exc_info:
        campaign_service.delete_campaign(1)

    assert "Failed to delete campaign" in str(exc_info.value)


def test_delete_campaign_exception(campaign_service, mock_campaign_repo):
    """Test delete campaign handles exceptions."""
    mock_campaign_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(CampaignServiceError) as exc_info:
        campaign_service.delete_campaign(1)

    assert "Error while deleting campaign" in str(exc_info.value)


def test_delete_campaign_no_related_entities(campaign_service, mock_campaign_repo, mock_class_repo,
                                             mock_diceset_repo, mock_dicelog_repo, sample_campaign):
    """Test deleting campaign with no related entities."""
    mock_campaign_repo.get_by_id.return_value = sample_campaign
    mock_dicelog_repo.list_by_campaign.return_value = []
    mock_diceset_repo.list_by_campaign.return_value = []
    mock_class_repo.list_by_campaign.return_value = []
    mock_campaign_repo.delete.return_value = sample_campaign

    result = campaign_service.delete_campaign(1)

    # Verify no deletions for related entities
    mock_dicelog_repo.delete.assert_not_called()
    mock_diceset_repo.delete.assert_not_called()
    mock_class_repo.delete.assert_not_called()
    mock_campaign_repo.delete.assert_called_once_with(1)
    assert result == sample_campaign
