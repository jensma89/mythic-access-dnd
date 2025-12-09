"""
test_class_service.py

Test for class service - business logic.
"""
import pytest
import uuid

from services.dnd_class.class_service import ClassService
from services.dnd_class.class_service_exceptions import (
    ClassNotFoundError,
    ClassCreateError,
    ClassUpdateError,
    ClassDeleteError,
    ClassServiceError
)
from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassSkills
from models.db_models.test_db import get_session as get_test_session
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from dependencies import ClassQueryParams
from auth.test_helpers import create_test_user, create_test_campaign


def test_create_class():
    """Test to create a new class."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    class_data = ClassCreate(
        name=f"Test Class {suffix}",
        dnd_class="Wizard",
        race="Elf",
        campaign_id=campaign.id,
        skills=ClassSkills(Intelligence=15, Wisdom=12)
    )
    class_data.set_user(user.id)

    created_class = service.create_class(class_data)

    assert created_class.name == f"Test Class {suffix}"
    assert created_class.dnd_class == "Wizard"
    assert created_class.id is not None


def test_get_class():
    """Test to get a class by ID."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    class_data = ClassCreate(
        name=f"Get Test Class {suffix}",
        dnd_class="Rogue",
        race="Halfling",
        campaign_id=campaign.id
    )
    class_data.set_user(user.id)
    created = service.create_class(class_data)

    result = service.get_class(created.id)

    assert result.id == created.id
    assert result.name == f"Get Test Class {suffix}"


def test_get_class_not_found():
    """Test get class with non-existent ID."""
    gen = get_test_session()
    session = next(gen)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    with pytest.raises(ClassNotFoundError):
        service.get_class(99999)


def test_list_classes():
    """Test to list all classes."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix1 = uuid.uuid4().hex[:8]
    class1_data = ClassCreate(
        name=f"List Class 1 {suffix1}",
        dnd_class="Warrior",
        race="Human",
        campaign_id=campaign.id
    )
    class1_data.set_user(user.id)
    service.create_class(class1_data)

    suffix2 = uuid.uuid4().hex[:8]
    class2_data = ClassCreate(
        name=f"List Class 2 {suffix2}",
        dnd_class="Cleric",
        race="Dwarf",
        campaign_id=campaign.id
    )
    class2_data.set_user(user.id)
    service.create_class(class2_data)

    filters = ClassQueryParams(campaign_id=campaign.id)
    classes = service.list_classes(filters)

    assert isinstance(classes, list)


def test_list_classes_with_filter():
    """Test list classes with name filter."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    class_data = ClassCreate(
        name=f"filtered_class_{suffix}",
        dnd_class="Paladin",
        race="Human",
        campaign_id=campaign.id
    )
    class_data.set_user(user.id)
    service.create_class(class_data)

    filters = ClassQueryParams(campaign_id=campaign.id, name=f"filtered_class_{suffix}")
    classes = service.list_classes(filters)

    assert len(classes) >= 1
    assert any(f"filtered_class_{suffix}" in c.name for c in classes)


def test_update_class():
    """Test to update a class."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    class_data = ClassCreate(
        name=f"update_test_{suffix}",
        dnd_class="Ranger",
        race="Elf",
        campaign_id=campaign.id
    )
    class_data.set_user(user.id)
    created_class = service.create_class(class_data)

    update_data = ClassUpdate(dnd_class="Druid", notes="Updated class")
    updated = service.update_class(created_class.id, update_data)

    assert updated is not None
    assert updated.id == created_class.id


def test_update_class_not_found():
    """Test update with non-existent class ID."""
    gen = get_test_session()
    session = next(gen)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    update_data = ClassUpdate(dnd_class="Barbarian")

    with pytest.raises((ClassNotFoundError, ClassServiceError)):
        service.update_class(99999, update_data)


def test_delete_class():
    """Test to delete a class."""
    gen = get_test_session()
    session = next(gen)

    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    suffix = uuid.uuid4().hex[:8]
    class_data = ClassCreate(
        name=f"Delete Test Class {suffix}",
        dnd_class="Monk",
        race="Human",
        campaign_id=campaign.id
    )
    class_data.set_user(user.id)
    created_class = service.create_class(class_data)

    deleted = service.delete_class(created_class.id)

    assert deleted is not None

    # Verify class is gone
    with pytest.raises(ClassNotFoundError):
        service.get_class(created_class.id)


def test_delete_class_not_found():
    """Test delete with non-existent class ID."""
    gen = get_test_session()
    session = next(gen)

    service = ClassService(
        class_repo=SqlAlchemyClassRepository(session),
        diceset_repo=SqlAlchemyDiceSetRepository(session),
        dicelog_repo=SqlAlchemyDiceLogRepository(session)
    )

    with pytest.raises((ClassNotFoundError, ClassDeleteError, ClassServiceError)):
        service.delete_class(99999)
