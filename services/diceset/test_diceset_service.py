# """
# test_diceset_service.py
# 
# Test for diceset service - business logic.
# """
# import pytest
# import uuid
# 
# from services.diceset.diceset_service import DiceSetService
# from services.diceset.diceset_service_exceptions import (
#     DiceSetNotFoundError,
#     DiceSetCreateError,
#     DiceSetUpdateError,
#     DiceSetDeleteError,
#     DiceSetServiceError
# )
# from models.schemas.diceset_schema import DiceSetCreate, DiceSetUpdate
# from models.db_models.test_db import get_session as get_test_session
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from auth.test_helpers import create_test_user, create_test_campaign
# from services.dnd_class.class_service import ClassService
# from models.schemas.dice_schema import DiceCreate
# from services.dice.dice_service import DiceService
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from models.schemas.class_schema import ClassCreate
# 
# 
# def test_create_diceset():
#     """Test to create a new dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class for the dice set
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Wizard",
#         race="Elf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     # Create dice set
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id,
#         dice_ids=[]
#     )
#     diceset_data.set_user(user.id)
# 
#     diceset = service.create_diceset(diceset_data)
# 
#     assert diceset.name == f"Test DiceSet {set_suffix}"
#     assert diceset.id is not None
# 
# 
# def test_get_diceset():
#     """Test to get a dice set by ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Rogue",
#         race="Halfling",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Get Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     created = service.create_diceset(diceset_data)
# 
#     result = service.get_diceset(created.id)
# 
#     assert result.id == created.id
#     assert result.name == f"Get Test DiceSet {set_suffix}"
# 
# 
# def test_get_diceset_not_found():
#     """Test get dice set with non-existent ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(DiceSetNotFoundError):
#         service.get_diceset(99999)
# 
# 
# def test_list_dicesets():
#     """Test to list all dice sets."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Cleric",
#         race="Dwarf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set1_suffix = uuid.uuid4().hex[:8]
#     diceset1_data = DiceSetCreate(
#         name=f"List DiceSet 1 {set1_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset1_data.set_user(user.id)
#     service.create_diceset(diceset1_data)
# 
#     set2_suffix = uuid.uuid4().hex[:8]
#     diceset2_data = DiceSetCreate(
#         name=f"List DiceSet 2 {set2_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset2_data.set_user(user.id)
#     service.create_diceset(diceset2_data)
# 
#     dicesets = service.list_dicesets(offset=0, limit=100)
# 
#     assert isinstance(dicesets, list)
# 
# 
# def test_list_dicesets_with_filter():
#     """Test list dice sets with offset and limit."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Fighter",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"filtered_diceset_{set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     service.create_diceset(diceset_data)
# 
#     dicesets = service.list_dicesets(offset=0, limit=10)
# 
#     assert isinstance(dicesets, list)
#     assert len(dicesets) <= 10
# 
# 
# def test_update_diceset():
#     """Test to update a dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Ranger",
#         race="Elf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"update_test_{set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     diceset = service.create_diceset(diceset_data)
# 
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = DiceSetUpdate(name=f"updated_diceset_{new_suffix}")
#     updated = service.update_diceset(diceset.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == diceset.id
# 
# 
# def test_update_diceset_not_found():
#     """Test update with non-existent dice set ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = DiceSetUpdate(name="new_name")
# 
#     with pytest.raises((DiceSetNotFoundError, DiceSetServiceError)):
#         service.update_diceset(99999, update_data)
# 
# 
# def test_delete_diceset():
#     """Test to delete a dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Monk",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Delete Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     diceset = service.create_diceset(diceset_data)
# 
#     deleted = service.delete_diceset(diceset.id)
# 
#     assert deleted is not None
# 
#     # Verify dice set is gone
#     with pytest.raises(DiceSetNotFoundError):
#         service.get_diceset(diceset.id)
# 
# 
# def test_delete_diceset_not_found():
#     """Test delete with non-existent dice set ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((DiceSetNotFoundError, DiceSetDeleteError, DiceSetServiceError)):
#         service.delete_diceset(99999)


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from services.diceset.diceset_service import DiceSetService
from services.diceset.diceset_service_exceptions import (
    DiceSetServiceError,
    DiceSetNotFoundError,
    DiceSetCreateError,
    DiceSetUpdateError,
    DiceSetDeleteError,
    DiceSetRollError
)
from models.schemas.diceset_schema import DiceSetCreate, DiceSetUpdate, DiceSetPublic, DiceSetRollResult
from models.schemas.dice_schema import DiceRollResult
from models.schemas.dicelog_schema import DiceLogCreate


@pytest.fixture
def mock_dice_repo():
    """Fixture for mocked dice repository."""
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
def diceset_service(mock_dice_repo, mock_diceset_repo, mock_dicelog_repo):
    """Fixture for DiceSetService instance with mocked repositories."""
    return DiceSetService(
        dice_repo=mock_dice_repo,
        diceset_repo=mock_diceset_repo,
        dicelog_repo=mock_dicelog_repo
    )


@pytest.fixture
def sample_diceset_data():
    """Fixture for sample dice set creation data."""
    diceset_data = DiceSetCreate(
        name="Attack Set",
        dnd_class_id=1,
        campaign_id=10,
        dice_ids=[1, 2, 3]
    )
    diceset_data.set_user(1)
    return diceset_data


@pytest.fixture
def sample_diceset():
    """Fixture for sample dice set."""
    return DiceSetPublic(
        id=1,
        name="Attack Set",
        dnd_class_id=1,
        campaign_id=10,
        user_id=1,
        dices=[]
    )


# Tests for create_diceset function
def test_create_diceset_success(diceset_service, mock_dice_repo, mock_diceset_repo, sample_diceset_data, sample_diceset):
    """Test successful dice set creation."""
    mock_diceset_repo.get_by_class_id.return_value = []
    mock_dice_repo.get_by_id.return_value = Mock(id=1, name="d20", sides=20)
    mock_diceset_repo.add.return_value = sample_diceset
    mock_diceset_repo.get_by_id.return_value = sample_diceset

    result = diceset_service.create_diceset(sample_diceset_data)

    mock_diceset_repo.get_by_class_id.assert_called_once_with(1)
    mock_diceset_repo.add.assert_called_once_with(sample_diceset_data)
    assert result.id == sample_diceset.id
    assert result.name == sample_diceset.name


def test_create_diceset_max_limit_reached(diceset_service, mock_diceset_repo, sample_diceset_data):
    """Test dice set creation fails when max 5 sets per class reached."""
    existing_sets = [Mock() for _ in range(5)]
    mock_diceset_repo.get_by_class_id.return_value = existing_sets

    with pytest.raises(DiceSetCreateError) as exc_info:
        diceset_service.create_diceset(sample_diceset_data)

    assert "Maximum of 5 dice sets" in str(exc_info.value)


def test_create_diceset_dice_not_found(diceset_service, mock_dice_repo, mock_diceset_repo, sample_diceset_data):
    """Test dice set creation fails when dice not found."""
    mock_diceset_repo.get_by_class_id.return_value = []
    mock_dice_repo.get_by_id.side_effect = [Mock(), None, Mock()]

    with pytest.raises(DiceSetNotFoundError) as exc_info:
        diceset_service.create_diceset(sample_diceset_data)

    assert "not found" in str(exc_info.value)


def test_create_diceset_exception(diceset_service, mock_diceset_repo, sample_diceset_data):
    """Test dice set creation handles exceptions."""
    mock_diceset_repo.get_by_class_id.side_effect = Exception("Database error")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.create_diceset(sample_diceset_data)

    assert "Error while creating dice set" in str(exc_info.value)


def test_create_diceset_with_quantities(diceset_service, mock_dice_repo, mock_diceset_repo, sample_diceset_data, sample_diceset):
    """Test dice set creation stores dice quantities."""
    mock_diceset_repo.get_by_class_id.return_value = []
    mock_dice_repo.get_by_id.return_value = Mock(id=1, name="d20", sides=20)
    mock_diceset_repo.add.return_value = sample_diceset
    mock_diceset_repo.get_by_id.return_value = sample_diceset

    result = diceset_service.create_diceset(sample_diceset_data)

    # Verify set_dice_quantities was called
    mock_diceset_repo.set_dice_quantities.assert_called_once()
    call_args = mock_diceset_repo.set_dice_quantities.call_args[0]
    assert call_args[0] == sample_diceset.id


# Tests for get_diceset function
def test_get_diceset_success(diceset_service, mock_diceset_repo, sample_diceset):
    """Test successful dice set retrieval."""
    mock_diceset_repo.get_by_id.return_value = sample_diceset

    result = diceset_service.get_diceset(1)

    mock_diceset_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_diceset.id
    assert result.name == sample_diceset.name


def test_get_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test get dice set raises error when not found."""
    mock_diceset_repo.get_by_id.return_value = None

    with pytest.raises(DiceSetNotFoundError) as exc_info:
        diceset_service.get_diceset(999)

    assert "Dice set with ID 999 not found" in str(exc_info.value)


def test_get_diceset_exception(diceset_service, mock_diceset_repo):
    """Test get dice set handles exceptions."""
    mock_diceset_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.get_diceset(1)

    assert "Error while fetching dice set" in str(exc_info.value)


# Tests for list_dicesets function
def test_list_dicesets_success(diceset_service, mock_diceset_repo):
    """Test successful dice set listing."""
    dicesets = [
        DiceSetPublic(id=1, name="Set 1", dnd_class_id=1, campaign_id=10, user_id=1, dices=[]),
        DiceSetPublic(id=2, name="Set 2", dnd_class_id=1, campaign_id=10, user_id=1, dices=[])
    ]
    mock_diceset_repo.list_all.return_value = dicesets

    result = diceset_service.list_dicesets(offset=0, limit=100)

    mock_diceset_repo.list_all.assert_called_once_with(offset=0, limit=100)
    assert len(result) == 2
    assert result[0].name == "Set 1"
    assert result[1].name == "Set 2"


def test_list_dicesets_empty(diceset_service, mock_diceset_repo):
    """Test dice set listing returns empty list."""
    mock_diceset_repo.list_all.return_value = []

    result = diceset_service.list_dicesets()

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_dicesets_exception(diceset_service, mock_diceset_repo):
    """Test list dice sets handles exceptions."""
    mock_diceset_repo.list_all.side_effect = Exception("Database error")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.list_dicesets()

    assert "Error while listing dice sets" in str(exc_info.value)


# Tests for update_diceset function
def test_update_diceset_success(diceset_service, mock_diceset_repo):
    """Test successful dice set update."""
    updated_diceset = DiceSetPublic(
        id=1,
        name="Updated Set",
        dnd_class_id=1,
        campaign_id=10,
        user_id=1,
        dices=[]
    )
    mock_diceset_repo.update.return_value = updated_diceset

    update_data = DiceSetUpdate(name="Updated Set")
    result = diceset_service.update_diceset(1, update_data)

    mock_diceset_repo.update.assert_called_once_with(1, update_data)
    assert result.id == 1
    assert result.name == "Updated Set"


def test_update_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test update dice set raises error when not found."""
    mock_diceset_repo.update.return_value = None

    update_data = DiceSetUpdate(name="new_name")

    with pytest.raises(DiceSetNotFoundError) as exc_info:
        diceset_service.update_diceset(999, update_data)

    assert "Dice set with ID 999 not found" in str(exc_info.value)


def test_update_diceset_exception(diceset_service, mock_diceset_repo):
    """Test update dice set handles exceptions."""
    mock_diceset_repo.update.side_effect = Exception("Database error")

    update_data = DiceSetUpdate(name="new_name")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.update_diceset(1, update_data)

    assert "Error while updating dice set" in str(exc_info.value)


# Tests for delete_diceset function
def test_delete_diceset_success(diceset_service, mock_diceset_repo, mock_dicelog_repo, sample_diceset):
    """Test successful dice set deletion with related dice logs."""
    mock_dicelog_repo.list_by_diceset.return_value = [Mock(id=1), Mock(id=2)]
    mock_diceset_repo.delete.return_value = sample_diceset

    result = diceset_service.delete_diceset(1)

    # Verify dice logs were deleted
    assert mock_dicelog_repo.delete.call_count == 2
    mock_diceset_repo.delete.assert_called_once_with(1)
    assert result == sample_diceset


def test_delete_diceset_not_found(diceset_service, mock_diceset_repo, mock_dicelog_repo):
    """Test delete dice set raises error when not found."""
    mock_dicelog_repo.list_by_diceset.return_value = []
    mock_diceset_repo.delete.return_value = None

    with pytest.raises(DiceSetNotFoundError) as exc_info:
        diceset_service.delete_diceset(999)

    assert "Dice set with ID 999 not found" in str(exc_info.value)


def test_delete_diceset_exception(diceset_service, mock_dicelog_repo):
    """Test delete dice set handles exceptions."""
    mock_dicelog_repo.list_by_diceset.side_effect = Exception("Database error")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.delete_diceset(1)

    assert "Error while deleting dice set" in str(exc_info.value)


def test_delete_diceset_no_logs(diceset_service, mock_diceset_repo, mock_dicelog_repo, sample_diceset):
    """Test deleting dice set with no related dice logs."""
    mock_dicelog_repo.list_by_diceset.return_value = []
    mock_diceset_repo.delete.return_value = sample_diceset

    result = diceset_service.delete_diceset(1)

    # Verify no deletions for dice logs
    mock_dicelog_repo.delete.assert_not_called()
    mock_diceset_repo.delete.assert_called_once_with(1)
    assert result == sample_diceset


# Tests for _log_roll function
def test_log_roll_success(diceset_service, mock_dicelog_repo):
    """Test successful dice set roll logging."""
    results = [
        DiceRollResult(id=1, name="d20", sides=20, result=15),
        DiceRollResult(id=2, name="d6", sides=6, result=4)
    ]

    diceset_service._log_roll(
        user_id=1,
        campaign_id=10,
        dnd_class_id=5,
        diceset_id=1,
        name="Attack Set",
        results=results,
        total=19
    )

    mock_dicelog_repo.log_roll.assert_called_once()
    call_args = mock_dicelog_repo.log_roll.call_args[0][0]
    assert call_args.user_id == 1
    assert call_args.campaign_id == 10
    assert call_args.dnd_class_id == 5
    assert call_args.diceset_id == 1
    assert call_args.result == 19


def test_log_roll_exception(diceset_service, mock_dicelog_repo):
    """Test log roll handles exceptions."""
    mock_dicelog_repo.log_roll.side_effect = Exception("Logging error")

    results = [DiceRollResult(id=1, name="d20", sides=20, result=15)]

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service._log_roll(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=1,
            name="Attack Set",
            results=results,
            total=15
        )

    assert "Error while logging dice set roll" in str(exc_info.value)


# Tests for roll_diceset function
def test_roll_diceset_success(diceset_service, mock_diceset_repo, mock_dicelog_repo):
    """Test successful dice set roll."""
    # Create mock dice set with dice entries using spec_set
    mock_dice1 = Mock()
    mock_dice1.id = 1
    mock_dice1.name = "d20"
    mock_dice1.sides = 20

    mock_dice2 = Mock()
    mock_dice2.id = 2
    mock_dice2.name = "d6"
    mock_dice2.sides = 6

    mock_entry1 = Mock()
    mock_entry1.dice = mock_dice1
    mock_entry1.quantity = 1

    mock_entry2 = Mock()
    mock_entry2.dice = mock_dice2
    mock_entry2.quantity = 2

    mock_diceset = Mock()
    mock_diceset.id = 1
    mock_diceset.name = "Attack Set"
    mock_diceset.dice_entries = [mock_entry1, mock_entry2]

    mock_diceset_repo.get_orm_by_id.return_value = mock_diceset

    with patch('services.diceset.diceset_service.randint', side_effect=[15, 4, 3]):
        result = diceset_service.roll_diceset(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=1
        )

    assert isinstance(result, DiceSetRollResult)
    assert result.diceset_id == 1
    assert result.name == "Attack Set"
    assert len(result.results) == 3
    assert result.total == 22  # 15 + 4 + 3


def test_roll_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test roll dice set raises error when not found."""
    mock_diceset_repo.get_orm_by_id.return_value = None

    with pytest.raises((DiceSetNotFoundError, DiceSetServiceError)):
        diceset_service.roll_diceset(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=999
        )


def test_roll_diceset_no_dices(diceset_service, mock_diceset_repo):
    """Test roll dice set raises error when set has no dices."""
    mock_diceset = Mock()
    mock_diceset.id = 1
    mock_diceset.name = "Empty Set"
    mock_diceset.dice_entries = []

    mock_diceset_repo.get_orm_by_id.return_value = mock_diceset

    with pytest.raises((DiceSetNotFoundError, DiceSetServiceError)):
        diceset_service.roll_diceset(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=1
        )


def test_roll_diceset_exception(diceset_service, mock_diceset_repo):
    """Test roll dice set handles exceptions."""
    mock_diceset_repo.get_orm_by_id.side_effect = Exception("Database error")

    with pytest.raises(DiceSetServiceError) as exc_info:
        diceset_service.roll_diceset(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=1
        )

    assert "Error while rolling dice set" in str(exc_info.value)


def test_roll_diceset_multiple_quantities(diceset_service, mock_diceset_repo, mock_dicelog_repo):
    """Test roll dice set with multiple quantities of same dice."""
    mock_dice = Mock()
    mock_dice.id = 1
    mock_dice.name = "d6"
    mock_dice.sides = 6

    mock_entry = Mock()
    mock_entry.dice = mock_dice
    mock_entry.quantity = 3

    mock_diceset = Mock()
    mock_diceset.id = 1
    mock_diceset.name = "Triple d6"
    mock_diceset.dice_entries = [mock_entry]

    mock_diceset_repo.get_orm_by_id.return_value = mock_diceset

    with patch('services.diceset.diceset_service.randint', side_effect=[2, 5, 4]):
        result = diceset_service.roll_diceset(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=1
        )

    assert len(result.results) == 3
    assert result.total == 11  # 2 + 5 + 4
    # Verify logging was called
    mock_dicelog_repo.log_roll.assert_called_once()
