# """
# test_dice_service.py
# 
# Test for dice service - business logic.
# """
# import pytest
# import uuid
# 
# from services.dice.dice_service import DiceService
# from services.dice.dice_service_exceptions import (
#     DiceNotFoundError,
#     DiceCreateError,
#     DiceUpdateError,
#     DiceDeleteError,
#     DiceServiceError
# )
# from models.schemas.dice_schema import DiceCreate, DiceUpdate
# from models.db_models.test_db import get_session as get_test_session
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# 
# 
# def test_create_dice():
#     """Test to create a new dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d20_{suffix}",
#         sides=20
#     )
#     dice = service.create_dice(dice_data)
# 
#     assert dice.name == f"d20_{suffix}"
#     assert dice.sides == 20
#     assert dice.id is not None
# 
# 
# def test_get_dice():
#     """Test to get a dice by ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d12_{suffix}",
#         sides=12
#     )
#     created = service.create_dice(dice_data)
# 
#     result = service.get_dice(created.id)
# 
#     assert result.id == created.id
#     assert result.name == f"d12_{suffix}"
#     assert result.sides == 12
# 
# 
# def test_get_dice_not_found():
#     """Test get dice with non-existent ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(DiceNotFoundError):
#         service.get_dice(99999)
# 
# 
# def test_list_dices():
#     """Test to list all dices."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix1 = uuid.uuid4().hex[:8]
#     dice1_data = DiceCreate(
#         name=f"d6_{suffix1}",
#         sides=6
#     )
#     service.create_dice(dice1_data)
# 
#     suffix2 = uuid.uuid4().hex[:8]
#     dice2_data = DiceCreate(
#         name=f"d8_{suffix2}",
#         sides=8
#     )
#     service.create_dice(dice2_data)
# 
#     dices = service.list_dices(offset=0, limit=100)
# 
#     assert isinstance(dices, list)
# 
# 
# def test_list_dices_with_filter():
#     """Test list dices with offset and limit."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d10_{suffix}",
#         sides=10
#     )
#     service.create_dice(dice_data)
# 
#     dices = service.list_dices(offset=0, limit=10)
# 
#     assert isinstance(dices, list)
#     assert len(dices) <= 10
# 
# 
# def test_update_dice():
#     """Test to update a dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d4_{suffix}",
#         sides=4
#     )
#     dice = service.create_dice(dice_data)
# 
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = DiceUpdate(name=f"d4_updated_{new_suffix}")
#     updated = service.update_dice(dice.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == dice.id
#     assert updated.name == f"d4_updated_{new_suffix}"
# 
# 
# def test_update_dice_not_found():
#     """Test update with non-existent dice ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = DiceUpdate(name="new_name")
# 
#     with pytest.raises((DiceNotFoundError, DiceServiceError)):
#         service.update_dice(99999, update_data)
# 
# 
# def test_delete_dice():
#     """Test to delete a dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d100_{suffix}",
#         sides=100
#     )
#     dice = service.create_dice(dice_data)
# 
#     deleted = service.delete_dice(dice.id)
# 
#     assert deleted is not None
# 
#     # Verify dice is gone
#     with pytest.raises(DiceNotFoundError):
#         service.get_dice(dice.id)
# 
# 
# def test_delete_dice_not_found():
#     """Test delete with non-existent dice ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((DiceNotFoundError, DiceDeleteError, DiceServiceError)):
#         service.delete_dice(99999)


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from services.dice.dice_service import DiceService
from services.dice.dice_service_exceptions import (
    DiceServiceError,
    DiceNotFoundError,
    DiceCreateError,
    DiceUpdateError,
    DiceDeleteError,
    DiceRollError
)
from models.schemas.dice_schema import DiceCreate, DiceUpdate, DicePublic, DiceRollResult
from models.schemas.dicelog_schema import DiceLogCreate


@pytest.fixture
def mock_dice_repo():
    """Fixture for mocked dice repository."""
    return Mock()


@pytest.fixture
def mock_log_repo():
    """Fixture for mocked dice log repository."""
    return Mock()


@pytest.fixture
def dice_service(mock_dice_repo, mock_log_repo):
    """Fixture for DiceService instance with mocked repositories."""
    return DiceService(
        repository=mock_dice_repo,
        log_repository=mock_log_repo
    )


@pytest.fixture
def dice_service_no_log(mock_dice_repo):
    """Fixture for DiceService instance without log repository."""
    return DiceService(
        repository=mock_dice_repo,
        log_repository=None
    )


@pytest.fixture
def sample_dice_data():
    """Fixture for sample dice creation data."""
    return DiceCreate(
        name="d20",
        sides=20
    )


@pytest.fixture
def sample_dice():
    """Fixture for sample dice."""
    return DicePublic(
        id=1,
        name="d20",
        sides=20
    )


# Tests for create_dice function
def test_create_dice_success(dice_service, mock_dice_repo, sample_dice_data, sample_dice):
    """Test successful dice creation."""
    mock_dice_repo.add.return_value = sample_dice

    result = dice_service.create_dice(sample_dice_data)

    mock_dice_repo.add.assert_called_once_with(sample_dice_data)
    assert result.id == sample_dice.id
    assert result.name == sample_dice.name
    assert result.sides == sample_dice.sides


def test_create_dice_exception(dice_service, mock_dice_repo, sample_dice_data):
    """Test dice creation handles exceptions."""
    mock_dice_repo.add.side_effect = Exception("Database error")

    with pytest.raises(DiceCreateError) as exc_info:
        dice_service.create_dice(sample_dice_data)

    assert "Error while creating dice" in str(exc_info.value)


# Tests for get_dice function
def test_get_dice_success(dice_service, mock_dice_repo, sample_dice):
    """Test successful dice retrieval."""
    mock_dice_repo.get_by_id.return_value = sample_dice

    result = dice_service.get_dice(1)

    mock_dice_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_dice.id
    assert result.name == sample_dice.name
    assert result.sides == sample_dice.sides


def test_get_dice_not_found(dice_service, mock_dice_repo):
    """Test get dice raises error when dice not found."""
    mock_dice_repo.get_by_id.return_value = None

    with pytest.raises(DiceNotFoundError) as exc_info:
        dice_service.get_dice(999)

    assert "Dice with ID 999 not found" in str(exc_info.value)


def test_get_dice_exception(dice_service, mock_dice_repo):
    """Test get dice handles exceptions."""
    mock_dice_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(DiceServiceError) as exc_info:
        dice_service.get_dice(1)

    assert "Error while fetching dice" in str(exc_info.value)


# Tests for list_dices function
def test_list_dices_success(dice_service, mock_dice_repo):
    """Test successful dice listing."""
    dices = [
        DicePublic(id=1, name="d6", sides=6),
        DicePublic(id=2, name="d20", sides=20)
    ]
    mock_dice_repo.list_all.return_value = dices

    result = dice_service.list_dices(offset=0, limit=100)

    mock_dice_repo.list_all.assert_called_once_with(offset=0, limit=100)
    assert len(result) == 2
    assert result[0].name == "d6"
    assert result[1].name == "d20"


def test_list_dices_empty(dice_service, mock_dice_repo):
    """Test dice listing returns empty list."""
    mock_dice_repo.list_all.return_value = []

    result = dice_service.list_dices()

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_dices_exception(dice_service, mock_dice_repo):
    """Test list dices handles exceptions."""
    mock_dice_repo.list_all.side_effect = Exception("Database error")

    with pytest.raises(DiceServiceError) as exc_info:
        dice_service.list_dices()

    assert "Error while listing dices" in str(exc_info.value)


# Tests for update_dice function
def test_update_dice_success(dice_service, mock_dice_repo):
    """Test successful dice update."""
    updated_dice = DicePublic(
        id=1,
        name="d20_updated",
        sides=20
    )
    mock_dice_repo.update.return_value = updated_dice

    update_data = DiceUpdate(name="d20_updated")
    result = dice_service.update_dice(1, update_data)

    mock_dice_repo.update.assert_called_once_with(1, update_data)
    assert result.id == 1
    assert result.name == "d20_updated"


def test_update_dice_not_found(dice_service, mock_dice_repo):
    """Test update dice raises error when dice not found."""
    mock_dice_repo.update.return_value = None

    update_data = DiceUpdate(name="new_name")

    with pytest.raises((DiceNotFoundError, DiceServiceError)):
        dice_service.update_dice(999, update_data)


def test_update_dice_exception(dice_service, mock_dice_repo):
    """Test update dice handles exceptions."""
    mock_dice_repo.update.side_effect = Exception("Database error")

    update_data = DiceUpdate(name="new_name")

    with pytest.raises(DiceServiceError) as exc_info:
        dice_service.update_dice(1, update_data)

    assert "Error while updating dice" in str(exc_info.value)


# Tests for delete_dice function
def test_delete_dice_success(dice_service, mock_dice_repo, sample_dice):
    """Test successful dice deletion."""
    mock_dice_repo.delete.return_value = sample_dice

    result = dice_service.delete_dice(1)

    mock_dice_repo.delete.assert_called_once_with(1)
    assert result == sample_dice


def test_delete_dice_not_found(dice_service, mock_dice_repo):
    """Test delete dice raises error when dice not found."""
    mock_dice_repo.delete.return_value = None

    with pytest.raises((DiceNotFoundError, DiceServiceError)):
        dice_service.delete_dice(999)


def test_delete_dice_exception(dice_service, mock_dice_repo):
    """Test delete dice handles exceptions."""
    mock_dice_repo.delete.side_effect = Exception("Database error")

    with pytest.raises(DiceServiceError) as exc_info:
        dice_service.delete_dice(1)

    assert "Error while deleting dice" in str(exc_info.value)


# Tests for _log_roll function
def test_log_roll_success(dice_service, mock_log_repo):
    """Test successful dice roll logging."""
    dice_service._log_roll(
        user_id=1,
        campaign_id=10,
        dnd_class_id=5,
        diceset_id=None,
        name="d20",
        result=15
    )

    mock_log_repo.log_roll.assert_called_once()
    call_args = mock_log_repo.log_roll.call_args[0][0]
    assert call_args.user_id == 1
    assert call_args.campaign_id == 10
    assert call_args.dnd_class_id == 5
    assert call_args.roll == "d20"
    assert call_args.result == 15


def test_log_roll_no_repository(dice_service_no_log):
    """Test log roll skips when no log repository."""
    # Should not raise an error
    dice_service_no_log._log_roll(
        user_id=1,
        campaign_id=10,
        dnd_class_id=5,
        diceset_id=None,
        name="d20",
        result=15
    )


def test_log_roll_exception(dice_service, mock_log_repo):
    """Test log roll handles exceptions."""
    mock_log_repo.log_roll.side_effect = Exception("Logging error")

    with pytest.raises(DiceServiceError) as exc_info:
        dice_service._log_roll(
            user_id=1,
            campaign_id=10,
            dnd_class_id=5,
            diceset_id=None,
            name="d20",
            result=15
        )

    assert "Error while logging dice roll" in str(exc_info.value)


# Tests for roll_dice function
def test_roll_dice_success(dice_service, mock_dice_repo, sample_dice):
    """Test successful dice roll."""
    mock_dice_repo.get_by_id.return_value = sample_dice

    with patch('services.dice.dice_service.randint', return_value=15):
        result = dice_service.roll_dice(
            dice_id=1,
            user_id=None,
            campaign_id=None,
            dnd_class_id=None
        )

    mock_dice_repo.get_by_id.assert_called_once_with(1)
    assert isinstance(result, DiceRollResult)
    assert result.id == sample_dice.id
    assert result.name == sample_dice.name
    assert result.sides == sample_dice.sides
    assert result.result == 15


def test_roll_dice_not_found(dice_service, mock_dice_repo):
    """Test roll dice raises error when dice not found."""
    mock_dice_repo.get_by_id.return_value = None

    with pytest.raises(DiceNotFoundError) as exc_info:
        dice_service.roll_dice(
            dice_id=999,
            user_id=1,
            campaign_id=10,
            dnd_class_id=5
        )

    assert "Dice with ID 999 not found" in str(exc_info.value)


def test_roll_dice_with_logging(dice_service, mock_dice_repo, mock_log_repo, sample_dice):
    """Test dice roll with logging."""
    mock_dice_repo.get_by_id.return_value = sample_dice

    with patch('services.dice.dice_service.randint', return_value=18):
        result = dice_service.roll_dice(
            dice_id=1,
            user_id=1,
            campaign_id=10,
            dnd_class_id=5
        )

    # Verify logging was called
    mock_log_repo.log_roll.assert_called_once()
    assert result.result == 18


def test_roll_dice_without_logging_partial_params(dice_service, mock_dice_repo, mock_log_repo, sample_dice):
    """Test dice roll without logging when some params are None."""
    mock_dice_repo.get_by_id.return_value = sample_dice

    with patch('services.dice.dice_service.randint', return_value=10):
        result = dice_service.roll_dice(
            dice_id=1,
            user_id=1,
            campaign_id=None,
            dnd_class_id=5
        )

    # Verify logging was not called
    mock_log_repo.log_roll.assert_not_called()
    assert result.result == 10


def test_roll_dice_result_in_range(dice_service, mock_dice_repo, sample_dice):
    """Test that roll result respects dice sides."""
    mock_dice_repo.get_by_id.return_value = sample_dice

    # Run multiple times to check randomness is within bounds
    with patch('services.dice.dice_service.randint') as mock_randint:
        mock_randint.return_value = 1
        result = dice_service.roll_dice(
            dice_id=1,
            user_id=None,
            campaign_id=None,
            dnd_class_id=None
        )

        # Verify randint was called with correct parameters
        mock_randint.assert_called_once_with(1, sample_dice.sides)
        assert result.result == 1
