"""
test_dices.py

Tests for dice endpoints.
"""
from fastapi.testclient import TestClient

from main import app
from dependencies import get_session as prod_get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token, create_test_campaign
from services.dice.dice_service import DiceService
from models.schemas.dice_schema import DiceCreate
from models.schemas.class_schema import ClassCreate, ClassSkills
from repositories.sql_dice_repository import SqlAlchemyDiceRepository
from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
from services.dnd_class.class_service import ClassService


# Override DB dependency
app.dependency_overrides[prod_get_session] = get_test_session
client = TestClient(app)


def auth_header(user):
    """Create the authentication header for a user."""
    token = get_test_token(user)
    return {"Authorization": f"Bearer {token}"}


def get_dice_service(session):
    """Factory to create DiceService with test session."""
    return DiceService(
        SqlAlchemyDiceRepository(session),
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
    payload = DiceCreate(
        name=name,
        sides=sides
    )
    return service.create_dice(payload)


def test_read_dice_success():
    """Test reading a dice successfully."""
    session = next(get_test_session())
    user = create_test_user(session)

    # Create a test dice
    dice = create_test_dice(session, "D20", 20)

    response = client.get(
        f"/dices/{dice.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dice.id
    assert data["sides"] == 20
    assert data["name"] == "D20"


def test_read_dice_not_found():
    """Test reading a non-existing dice returns 404."""
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.get(
        "/dices/99999",
        headers=auth_header(user)
    )
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert (
            "not found" in detail.lower()
            or "dice" in detail.lower())


def test_read_dices_list():
    """Test listing all dices."""
    session = next(get_test_session())
    user = create_test_user(session)

    # Create some test dices
    create_test_dice(session, "D4", 4)
    create_test_dice(session, "D8", 8)

    response = client.get(
        "/dices/",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_roll_dice_success():
    """Test rolling a dice successfully."""
    session = next(get_test_session())
    user = create_test_user(session)

    # Create a test dice
    dice = create_test_dice(session, "D6", 6)

    response = client.post(
        f"/dices/{dice.id}/roll",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "id" in data
    assert data["id"] == dice.id
    assert isinstance(data["result"], int)
    assert 1 <= data["result"] <= 6


def test_roll_dice_not_found():
    """Test rolling a non-existing dice returns 404."""
    session = next(get_test_session())
    user = create_test_user(session)

    response = client.post(
        "/dices/99999/roll",
        headers=auth_header(user)
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_roll_dice_with_campaign():
    """Test rolling a dice with campaign_id parameter."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    # Create a test dice
    dice = create_test_dice(session, "D12", 12)

    response = client.post(
        f"/dices/{dice.id}/roll?campaign_id={campaign.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], int)
    assert 1 <= data["result"] <= 12


def test_roll_dice_with_class():
    """Test rolling a dice with class_id parameter."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    # Create a class
    class_service = get_class_service(session)
    payload = ClassCreate(
        name="Testchar",
        dnd_class="Fighter",
        race="Human",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)
    dnd_class = class_service.create_class(payload)

    # Create a test dice
    dice = create_test_dice(session, "D10", 10)

    response = client.post(
        f"/dices/{dice.id}/roll?class_id={dnd_class.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], int)
    assert 1 <= data["result"] <= 10


def test_roll_dice_with_campaign_and_class():
    """Test rolling a dice with both campaign_id and class_id."""
    session = next(get_test_session())
    user = create_test_user(session)
    campaign = create_test_campaign(session, user)

    # Create a class
    class_service = get_class_service(session)
    payload = ClassCreate(
        name="Testchar2",
        dnd_class="Wizard",
        race="Elf",
        campaign_id=campaign.id,
        skills=ClassSkills()
    )
    payload.set_user(user.id)
    dnd_class = class_service.create_class(payload)

    # Create a test dice
    dice = create_test_dice(session, "D100", 100)

    response = client.post(
        f"/dices/{dice.id}/roll?campaign_id={campaign.id}&class_id={dnd_class.id}",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], int)
    assert 1 <= data["result"] <= 100


def test_read_dices_pagination():
    """Test pagination for dice list."""
    session = next(get_test_session())
    user = create_test_user(session)

    # Create multiple test dices
    for i in range(10):
        create_test_dice(session, f"D{i+4}", i+4)

    response = client.get(
        "/dices/?offset=0&limit=5",
        headers=auth_header(user)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_roll_dice_multiple_times():
    """Test rolling the same dice multiple times
    produces different results."""
    session = next(get_test_session())
    user = create_test_user(session)

    # Create a test dice with many sides
    dice = create_test_dice(session, "D20", 20)

    results = []
    for _ in range(10):
        response = client.post(
            f"/dices/{dice.id}/roll",
            headers=auth_header(user)
        )
        assert response.status_code == 200
        results.append(response.json()["result"])

    # Check all results are valid
    assert all(1 <= r <= 20 for r in results)
    # Check we got at least some variation (not all same)
    assert len(set(results)) > 1
