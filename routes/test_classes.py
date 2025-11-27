"""
test_classes.py

Tests for class endpoints.
"""
from fastapi.testclient import TestClient

from main import app
from dependencies import get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
from services.class_service import ClassService
from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassSkills
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository


# Override DB dependency
app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


def auth_header(user):
    """Create the authentication header for a user."""
    token = get_test_token(user)
    return {"Authorization": f"Bearer {token}"}


def get_class_service(session):
    """Factory to create ClassService with test session."""
    return ClassService(
        SqlAlchemyClassRepository(session),
        SqlAlchemyDiceSetRepository(session),
        SqlAlchemyDiceLogRepository(session)
    )


def test_create_class():
    """Test creating a new class."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    # Create payload with required skills
    payload = ClassCreate(
        name="Wizard",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)

    response = client.post(
        "/classes/",
        json=payload.model_dump(),
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Wizard"
    assert data["user_id"] == user.id


def test_read_class_success():
    """Test reading a class successfully."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = get_class_service(session)

    payload = ClassCreate(
        name="Fighter",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)
    dnd_class = service.create_class(payload)

    response = client.get(
        f"/classes/{dnd_class.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["id"] == dnd_class.id


def test_read_class_not_found():
    """Test reading a non-existing class returns 404."""
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.get(
        "/classes/9999",
        headers=auth_header(user)
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_class_success():
    """Test updating a class successfully."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = get_class_service(session)

    payload = ClassCreate(
        name="Rogue",
        race="Elf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)
    dnd_class = service.create_class(payload)

    update_payload = ClassUpdate(
        notes="Updated stealth master"
    )

    response = client.patch(
        f"/classes/{dnd_class.id}",
        json=update_payload.model_dump(exclude_unset=True),
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["notes"] == "Updated stealth master"


def test_update_class_forbidden():
    """Test that updating a class
    by another user is forbidden."""
    session = next(get_test_session())
    owner = create_test_user(session)
    other = create_test_user(session)
    campaign = create_test_campaign(session, owner)

    service = get_class_service(session)

    payload = ClassCreate(
        name="Paladin",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(owner.id)
    dnd_class = service.create_class(payload)

    update_payload = ClassUpdate(notes="Hacked!")

    response = client.patch(
        f"/classes/{dnd_class.id}",
        json=update_payload.model_dump(exclude_unset=True),
        headers=auth_header(other)
    )
    assert response.status_code == 403


def test_delete_class_success():
    """Test deleting a class successfully."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    service = get_class_service(session)

    payload = ClassCreate(
        name="Cleric",
        race="Dwarf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)
    dnd_class = service.create_class(payload)

    response = client.delete(
        f"/classes/{dnd_class.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    assert response.json()["id"] == dnd_class.id


def test_delete_class_forbidden():
    """Test that deleting a class
    by another user is forbidden."""
    session = next(get_test_session())
    owner = create_test_user(session)
    other = create_test_user(session)
    campaign = create_test_campaign(session, owner)

    service = get_class_service(session)

    payload = ClassCreate(
        name="Bard",
        race="Halfling",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(owner.id)
    dnd_class = service.create_class(payload)

    response = client.delete(
        f"/classes/{dnd_class.id}",
        headers=auth_header(other)
    )
    assert response.status_code == 403
