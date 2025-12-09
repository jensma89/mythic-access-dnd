"""
test_dicelogs.py

Tests for dicelog endpoints.
"""
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from main import app
from dependencies import get_session as prod_get_session
from models.db_models.test_db import get_session as get_test_session
from models.db_models.test_db import test_engine
from sqlmodel import Session
from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from models.schemas.dicelog_schema import DiceLogCreate
from models.schemas.dice_schema import DiceCreate
from models.schemas.diceset_schema import DiceSetCreate
from models.schemas.class_schema import ClassCreate, ClassSkills
from services.dice.dice_service import DiceService
from services.diceset.diceset_service import DiceSetService
from services.dnd_class.class_service import ClassService


# Override DB dependency
app.dependency_overrides[prod_get_session] = get_test_session


def auth_header(user):
    """Create the authentication header for a user."""
    token = get_test_token(user)
    return {"Authorization": f"Bearer {token}"}


def get_dicelog_repo(session):
    """Factory to create DiceLogRepository with test session."""
    return SqlAlchemyDiceLogRepository(session)


def get_dice_service(session):
    """Factory to create DiceService with test session."""
    return DiceService(
        SqlAlchemyDiceRepository(session),
        SqlAlchemyDiceLogRepository(session)
    )


def get_diceset_service(session):
    """Factory to create DiceSetService with test session."""
    return DiceSetService(
        SqlAlchemyDiceRepository(session),
        SqlAlchemyDiceSetRepository(session),
        SqlAlchemyDiceLogRepository(session)
    )


def get_class_service(session):
    """Factory to create ClassService with test session."""
    return ClassService(
        SqlAlchemyClassRepository(session),
        SqlAlchemyDiceSetRepository(session),
        SqlAlchemyDiceLogRepository(session)
    )


def create_test_dice(session, name="D6", sides=6):
    """Create a test dice."""
    service = get_dice_service(session)
    payload = DiceCreate(name=name, sides=sides)
    return service.create_dice(payload)


def create_test_diceset(session, user, dnd_class, campaign, name="TestSet", dice_ids=None):
    """Create a test diceset."""
    service = get_diceset_service(session)
    payload = DiceSetCreate(
        name=name,
        dnd_class_id=dnd_class.id,
        campaign_id=campaign.id,
        dice_ids=dice_ids or []
    )
    payload.set_user(user.id)
    return service.create_diceset(payload)


def create_test_dicelog(session, user, campaign, dnd_class, diceset=None, roll="D6: 4", result=4):
    """Create a test dice log entry directly in the repository."""
    repo = get_dicelog_repo(session)
    log_entry = DiceLogCreate(
        user_id=user.id,
        campaign_id=campaign.id,
        dnd_class_id=dnd_class.id,
        diceset_id=diceset.id if diceset else None,
        roll=roll,
        result=result,
        timestamp=datetime.now(timezone.utc)
    )
    return repo.log_roll(log_entry)


def test_list_logs_empty():
    """Test listing logs when there are none."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    response = client.get(
        "/dicelogs/",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # User should have no logs yet
    assert len(data) == 0


def test_list_logs_with_entries():
    """Test listing logs when entries exist."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)
    # Create class
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar",
        dnd_class="Warrior",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(user.id)
    dnd_class = class_service.create_class(class_payload)

    # Create some log entries
    create_test_dicelog(session, user, campaign, dnd_class, roll="D6: 3", result=3)
    create_test_dicelog(session, user, campaign, dnd_class, roll="D8: 5", result=5)
    create_test_dicelog(session, user, campaign, dnd_class, roll="D20: 15", result=15)

    response = client.get(
        "/dicelogs/",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_list_logs_pagination():
    """Test pagination for dice logs."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)
    # Create class
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar2",
        dnd_class="Mage",
        race="Elf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(user.id)
    dnd_class = class_service.create_class(class_payload)

    # Create multiple log entries
    for i in range(10):
        create_test_dicelog(
            session, user, campaign, dnd_class,
            roll=f"D20: {i+1}", result=i+1
        )

    # Test pagination with limit
    response = client.get(
        "/dicelogs/?offset=0&limit=5",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

    # Test pagination with offset
    response = client.get(
        "/dicelogs/?offset=5&limit=5",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_logs_only_own():
    """Test that users only see their own logs."""
    client = TestClient(app)
    session = Session(test_engine)
    user1 = create_test_user(session)
    user2 = create_test_user(session)
    campaign1 = create_test_campaign(session, user1)
    campaign2 = create_test_campaign(session, user2)
    # Create class for user1
    class_service = get_class_service(session)
    class_payload1 = ClassCreate(
        name="TestChar3",
        dnd_class="Rogue",
        race="Halfling",
        campaign_id=campaign1.id,
        skills=ClassSkills()
    )
    class_payload1.set_user(user1.id)
    dnd_class1 = class_service.create_class(class_payload1)

    # Create class for user2
    class_payload2 = ClassCreate(
        name="TestChar4",
        dnd_class="Paladin",
        race="Human",
        campaign_id=campaign2.id,
        skills=ClassSkills()
    )
    class_payload2.set_user(user2.id)
    dnd_class2 = class_service.create_class(class_payload2)

    # Create logs for both users
    create_test_dicelog(session, user1, campaign1, dnd_class1, roll="User1: D6", result=3)
    create_test_dicelog(session, user2, campaign2, dnd_class2, roll="User2: D8", result=5)

    # User1 should only see their own logs
    response = client.get(
        "/dicelogs/",
        headers=auth_header(user1)
    )
    assert response.status_code == 200
    data = response.json()
    for log in data:
        assert log["user_id"] == user1.id


def test_get_log_success():
    """Test getting a single log by ID."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)
    # Create class
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar5",
        dnd_class="Ranger",
        race="Elf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(user.id)
    dnd_class = class_service.create_class(class_payload)

    # Create a log entry
    log = create_test_dicelog(session, user, campaign, dnd_class, roll="D20: 18", result=18)

    response = client.get(
        f"/dicelogs/{log.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == log.id
    assert data["user_id"] == user.id
    assert data["result"] == 18


def test_get_log_not_found():
    """Test getting a non-existing log returns 404."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    response = client.get(
        "/dicelogs/99999",
        headers=auth_header(user)
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_log_forbidden():
    """Test that accessing another user's log is forbidden."""
    client = TestClient(app)
    session = Session(test_engine)
    owner = create_test_user(session)
    other = create_test_user(session)
    campaign = create_test_campaign(session, owner)
    # Create class for owner
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar6",
        dnd_class="Bard",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(owner.id)
    dnd_class = class_service.create_class(class_payload)

    # Create a log entry for owner
    log = create_test_dicelog(session, owner, campaign, dnd_class, roll="D6: 4", result=4)

    # Try to access as other user
    response = client.get(
        f"/dicelogs/{log.id}",
        headers=auth_header(other)
    )
    assert response.status_code == 403
    assert "not allowed" in response.json()["detail"].lower()


def test_list_logs_with_diceset():
    """Test that logs with diceset_id are returned correctly."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)
    # Create class
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar7",
        dnd_class="Cleric",
        race="Dwarf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(user.id)
    dnd_class = class_service.create_class(class_payload)

    # Create dice and diceset
    d6 = create_test_dice(session, "D6", 6)
    diceset = create_test_diceset(
        session, user, dnd_class, campaign, "TestSet", [d6.id]
    )

    # Create log with diceset reference
    create_test_dicelog(
        session, user, campaign, dnd_class,
        diceset=diceset, roll="TestSet: [4]", result=4
    )

    response = client.get(
        "/dicelogs/",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    # Find the log with our diceset
    diceset_logs = [log for log in data if log.get("diceset_id") == diceset.id]
    assert len(diceset_logs) >= 1
    assert diceset_logs[0]["diceset_id"] == diceset.id


def test_list_logs_with_single_dice():
    """Test that logs without diceset_id (single dice rolls) work correctly."""
    client = TestClient(app)
    session = Session(test_engine)
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)
    # Create class
    class_service = get_class_service(session)
    class_payload = ClassCreate(
        name="TestChar8",
        dnd_class="Monk",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    class_payload.set_user(user.id)
    dnd_class = class_service.create_class(class_payload)

    # Create log without diceset (single dice roll)
    create_test_dicelog(
        session, user, campaign, dnd_class,
        diceset=None, roll="D20: 15", result=15
    )

    response = client.get(
        "/dicelogs/",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    # Find logs without diceset
    single_dice_logs = [log for log in data if log.get("diceset_id") is None]
    assert len(single_dice_logs) >= 1

