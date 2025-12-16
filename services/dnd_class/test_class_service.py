# """
# test_class_service.py
# 
# Test for class service - business logic.
# """
# import pytest
# import uuid
# 
# from services.dnd_class.class_service import ClassService
# from services.dnd_class.class_service_exceptions import (
#     ClassNotFoundError,
#     ClassCreateError,
#     ClassUpdateError,
#     ClassDeleteError,
#     ClassServiceError
# )
# from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassSkills
# from models.db_models.test_db import get_session as get_test_session
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from dependencies import ClassQueryParams
# from auth.test_helpers import create_test_user, create_test_campaign
# 
# 
# def test_create_class():
#     """Test to create a new class."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Wizard",
#         race="Elf",
#         campaign_id=campaign.id,
#         skills=ClassSkills(Intelligence=15, Wisdom=12)
#     )
#     class_data.set_user(user.id)
# 
#     created_class = service.create_class(class_data)
# 
#     assert created_class.name == f"Test Class {suffix}"
#     assert created_class.dnd_class == "Wizard"
#     assert created_class.id is not None
# 
# 
# def test_get_class():
#     """Test to get a class by ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Get Test Class {suffix}",
#         dnd_class="Rogue",
#         race="Halfling",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     created = service.create_class(class_data)
# 
#     result = service.get_class(created.id)
# 
#     assert result.id == created.id
#     assert result.name == f"Get Test Class {suffix}"
# 
# 
# def test_get_class_not_found():
#     """Test get class with non-existent ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(ClassNotFoundError):
#         service.get_class(99999)
# 
# 
# def test_list_classes():
#     """Test to list all classes."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix1 = uuid.uuid4().hex[:8]
#     class1_data = ClassCreate(
#         name=f"List Class 1 {suffix1}",
#         dnd_class="Warrior",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class1_data.set_user(user.id)
#     service.create_class(class1_data)
# 
#     suffix2 = uuid.uuid4().hex[:8]
#     class2_data = ClassCreate(
#         name=f"List Class 2 {suffix2}",
#         dnd_class="Cleric",
#         race="Dwarf",
#         campaign_id=campaign.id
#     )
#     class2_data.set_user(user.id)
#     service.create_class(class2_data)
# 
#     filters = ClassQueryParams(campaign_id=campaign.id)
#     classes = service.list_classes(filters)
# 
#     assert isinstance(classes, list)
# 
# 
# def test_list_classes_with_filter():
#     """Test list classes with name filter."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"filtered_class_{suffix}",
#         dnd_class="Paladin",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     service.create_class(class_data)
# 
#     filters = ClassQueryParams(campaign_id=campaign.id, name=f"filtered_class_{suffix}")
#     classes = service.list_classes(filters)
# 
#     assert len(classes) >= 1
#     assert any(f"filtered_class_{suffix}" in c.name for c in classes)
# 
# 
# def test_update_class():
#     """Test to update a class."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"update_test_{suffix}",
#         dnd_class="Ranger",
#         race="Elf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     created_class = service.create_class(class_data)
# 
#     update_data = ClassUpdate(dnd_class="Druid", notes="Updated class")
#     updated = service.update_class(created_class.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == created_class.id
# 
# 
# def test_update_class_not_found():
#     """Test update with non-existent class ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = ClassUpdate(dnd_class="Barbarian")
# 
#     with pytest.raises((ClassNotFoundError, ClassServiceError)):
#         service.update_class(99999, update_data)
# 
# 
# def test_delete_class():
#     """Test to delete a class."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Delete Test Class {suffix}",
#         dnd_class="Monk",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     created_class = service.create_class(class_data)
# 
#     deleted = service.delete_class(created_class.id)
# 
#     assert deleted is not None
# 
#     # Verify class is gone
#     with pytest.raises(ClassNotFoundError):
#         service.get_class(created_class.id)
# 
# 
# def test_delete_class_not_found():
#     """Test delete with non-existent class ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((ClassNotFoundError, ClassDeleteError, ClassServiceError)):
#         service.delete_class(99999)


# Independent functional unit tests with mocks
import pytest
from unittest.mock import Mock
from services.dnd_class.class_service import ClassService
from services.dnd_class.class_service_exceptions import (
    ClassServiceError,
    ClassNotFoundError,
    ClassCreateError,
    ClassUpdateError,
    ClassDeleteError
)
from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassPublic, ClassSkills
from dependencies import ClassQueryParams


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
def class_service(mock_class_repo, mock_diceset_repo, mock_dicelog_repo):
    """Fixture for ClassService instance with mocked repositories."""
    return ClassService(
        class_repo=mock_class_repo,
        diceset_repo=mock_diceset_repo,
        dicelog_repo=mock_dicelog_repo
    )


@pytest.fixture
def sample_class_data():
    """Fixture for sample class creation data."""
    class_data = ClassCreate(
        name="Test Wizard",
        dnd_class="Wizard",
        race="Elf",
        campaign_id=10
    )
    class_data.set_user(1)
    return class_data


@pytest.fixture
def sample_class():
    """Fixture for sample class."""
    return ClassPublic(
        id=1,
        name="Test Wizard",
        dnd_class="Wizard",
        race="Elf",
        campaign_id=10,
        user_id=1,
        skills=ClassSkills(Intelligence=15, Wisdom=12)
    )


# Tests for create_class function
def test_create_class_success(class_service, mock_class_repo, sample_class_data, sample_class):
    """Test successful class creation."""
    mock_class_repo.get_by_campaign_id.return_value = []
    mock_class_repo.add.return_value = sample_class

    result = class_service.create_class(sample_class_data)

    mock_class_repo.get_by_campaign_id.assert_called_once_with(10)
    mock_class_repo.add.assert_called_once_with(sample_class_data)
    assert result.id == sample_class.id
    assert result.name == sample_class.name
    assert result.dnd_class == sample_class.dnd_class


def test_create_class_max_limit_reached(class_service, mock_class_repo, sample_class_data):
    """Test class creation fails when max 4 classes per campaign reached."""
    existing_classes = [Mock() for _ in range(4)]
    mock_class_repo.get_by_campaign_id.return_value = existing_classes

    with pytest.raises((ClassCreateError, ClassServiceError)):
        class_service.create_class(sample_class_data)


def test_create_class_repository_returns_none(class_service, mock_class_repo, sample_class_data):
    """Test class creation fails when repository returns None."""
    mock_class_repo.get_by_campaign_id.return_value = []
    mock_class_repo.add.return_value = None

    with pytest.raises((ClassCreateError, ClassServiceError)):
        class_service.create_class(sample_class_data)


def test_create_class_exception(class_service, mock_class_repo, sample_class_data):
    """Test class creation handles exceptions."""
    mock_class_repo.get_by_campaign_id.side_effect = Exception("Database error")

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.create_class(sample_class_data)

    assert "while create a dnd dnd_class" in str(exc_info.value)


# Tests for get_class function
def test_get_class_success(class_service, mock_class_repo, sample_class):
    """Test successful class retrieval."""
    mock_class_repo.get_by_id.return_value = sample_class

    result = class_service.get_class(1)

    mock_class_repo.get_by_id.assert_called_once_with(1)
    assert result.id == sample_class.id
    assert result.name == sample_class.name


def test_get_class_not_found(class_service, mock_class_repo):
    """Test get class raises error when class not found."""
    mock_class_repo.get_by_id.return_value = None

    with pytest.raises(ClassNotFoundError) as exc_info:
        class_service.get_class(999)

    assert "Class with ID 999 not found" in str(exc_info.value)


def test_get_class_exception(class_service, mock_class_repo):
    """Test get class handles exceptions."""
    mock_class_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.get_class(1)

    assert "Error while retrieving dnd_class" in str(exc_info.value)


# Tests for list_classes function
def test_list_classes_success(class_service, mock_class_repo):
    """Test successful class listing."""
    classes = [
        ClassPublic(id=1, name="Wizard 1", dnd_class="Wizard", race="Elf", campaign_id=10, user_id=1, skills=ClassSkills()),
        ClassPublic(id=2, name="Rogue 1", dnd_class="Rogue", race="Halfling", campaign_id=10, user_id=1, skills=ClassSkills())
    ]
    mock_class_repo.list_all.return_value = classes

    filters = ClassQueryParams(campaign_id=10)
    result = class_service.list_classes(filters, offset=0, limit=100)

    mock_class_repo.list_all.assert_called_once()
    assert len(result) == 2
    assert result[0].name == "Wizard 1"
    assert result[1].name == "Rogue 1"


def test_list_classes_with_filters(class_service, mock_class_repo):
    """Test class listing with name filter."""
    classes = [
        ClassPublic(id=1, name="Filtered Wizard", dnd_class="Wizard", race="Elf", campaign_id=10, user_id=1, skills=ClassSkills())
    ]
    mock_class_repo.list_all.return_value = classes

    filters = ClassQueryParams(campaign_id=10, name="Filtered")
    result = class_service.list_classes(filters, offset=5, limit=20)

    mock_class_repo.list_all.assert_called_once()
    assert len(result) == 1
    assert result[0].name == "Filtered Wizard"


def test_list_classes_empty(class_service, mock_class_repo):
    """Test class listing returns empty list."""
    mock_class_repo.list_all.return_value = []

    filters = ClassQueryParams(campaign_id=10)
    result = class_service.list_classes(filters)

    assert isinstance(result, list)
    assert len(result) == 0


def test_list_classes_exception(class_service, mock_class_repo):
    """Test list classes handles exceptions."""
    mock_class_repo.list_all.side_effect = Exception("Database error")

    filters = ClassQueryParams(campaign_id=10)

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.list_classes(filters)

    assert "Error while listing classes" in str(exc_info.value)


# Tests for update_class function
def test_update_class_success(class_service, mock_class_repo):
    """Test successful class update."""
    updated_class = ClassPublic(
        id=1,
        name="Updated Wizard",
        dnd_class="Sorcerer",
        race="Elf",
        campaign_id=10,
        user_id=1,
        skills=ClassSkills()
    )
    mock_class_repo.update.return_value = updated_class

    update_data = ClassUpdate(name="Updated Wizard", dnd_class="Sorcerer")
    result = class_service.update_class(1, update_data)

    mock_class_repo.update.assert_called_once_with(1, update_data)
    assert result.id == 1
    assert result.name == "Updated Wizard"
    assert result.dnd_class == "Sorcerer"


def test_update_class_not_found(class_service, mock_class_repo):
    """Test update class raises error when class not found."""
    mock_class_repo.update.return_value = None

    update_data = ClassUpdate(name="New Name")

    with pytest.raises((ClassNotFoundError, ClassServiceError)):
        class_service.update_class(999, update_data)


def test_update_class_exception(class_service, mock_class_repo):
    """Test update class handles exceptions."""
    mock_class_repo.update.side_effect = Exception("Database error")

    update_data = ClassUpdate(name="New Name")

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.update_class(1, update_data)

    assert "Error while updating dnd_class" in str(exc_info.value)


# Tests for delete_class function
def test_delete_class_success(class_service, mock_class_repo, mock_diceset_repo,
                              mock_dicelog_repo, sample_class):
    """Test successful class deletion with related entities."""
    # Setup mocks
    mock_class_repo.get_by_id.return_value = sample_class
    mock_dicelog_repo.list_by_class.return_value = [Mock(id=1), Mock(id=2)]

    diceset1 = Mock(id=10)
    diceset2 = Mock(id=11)
    mock_diceset_repo.list_by_class.return_value = [diceset1, diceset2]

    mock_dicelog_repo.list_by_diceset.side_effect = [
        [Mock(id=3), Mock(id=4)],  # Logs for diceset1
        [Mock(id=5)]                # Logs for diceset2
    ]

    mock_class_repo.delete.return_value = sample_class

    result = class_service.delete_class(1)

    # Verify deletion order: dice logs by class, dice logs by diceset, dice sets, class
    assert mock_dicelog_repo.delete.call_count == 5  # 2 from class + 3 from dicesets
    assert mock_diceset_repo.delete.call_count == 2
    mock_class_repo.delete.assert_called_once_with(1)
    assert result == sample_class


def test_delete_class_not_found(class_service, mock_class_repo):
    """Test delete class raises error when class not found."""
    mock_class_repo.get_by_id.return_value = None

    with pytest.raises(ClassNotFoundError) as exc_info:
        class_service.delete_class(999)

    assert "Class with ID 999 not found" in str(exc_info.value)


def test_delete_class_deletion_fails(class_service, mock_class_repo, mock_diceset_repo,
                                     mock_dicelog_repo, sample_class):
    """Test delete class when final deletion returns None."""
    mock_class_repo.get_by_id.return_value = sample_class
    mock_dicelog_repo.list_by_class.return_value = []
    mock_diceset_repo.list_by_class.return_value = []
    mock_class_repo.delete.return_value = None

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.delete_class(1)

    assert "deleting dnd_class" in str(exc_info.value)


def test_delete_class_exception(class_service, mock_class_repo):
    """Test delete class handles exceptions."""
    mock_class_repo.get_by_id.side_effect = Exception("Database error")

    with pytest.raises(ClassServiceError) as exc_info:
        class_service.delete_class(1)

    assert "Error while deleting dnd_class" in str(exc_info.value)


def test_delete_class_no_related_entities(class_service, mock_class_repo, mock_diceset_repo,
                                          mock_dicelog_repo, sample_class):
    """Test deleting class with no related entities."""
    mock_class_repo.get_by_id.return_value = sample_class
    mock_dicelog_repo.list_by_class.return_value = []
    mock_diceset_repo.list_by_class.return_value = []
    mock_class_repo.delete.return_value = sample_class

    result = class_service.delete_class(1)

    # Verify no deletions for related entities
    mock_dicelog_repo.delete.assert_not_called()
    mock_diceset_repo.delete.assert_not_called()
    mock_class_repo.delete.assert_called_once_with(1)
    assert result == sample_class
