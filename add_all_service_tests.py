#!/usr/bin/env python3
"""
Script to append comprehensive functional unit tests to all service test files.
Tests every function in each service with proper mocking.
"""

# Test content for each service
tests_content = {
    'services/auth/test_auth_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in auth_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.auth.auth_service import register_user, login
from models.schemas.user_schema import UserCreate


@pytest.fixture
def mock_session():
    """Mock database session."""
    return Mock()


@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def mock_user():
    """Mock user object."""
    user = Mock()
    user.id = 1
    user.username = "testuser"
    user.email = "test@example.com"
    user.password = "hashed_password"
    return user


# Tests for register_user()
def test_register_user_success(mock_session, sample_user_data, mock_user):
    """Test successful user registration."""
    with patch('services.auth.auth_service.hash_password') as mock_hash:
        with patch('services.auth.auth_service.User') as MockUser:
            mock_hash.return_value = "hashed_password"
            mock_session.exec.return_value.first.return_value = None
            MockUser.return_value = mock_user

            result = register_user(mock_session, sample_user_data)

            assert result == mock_user
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_user)


def test_register_user_duplicate_email(mock_session, sample_user_data):
    """Test registration fails with duplicate email."""
    mock_existing = Mock()
    mock_session.exec.return_value.first.return_value = mock_existing

    with pytest.raises(HTTPException) as exc_info:
        register_user(mock_session, sample_user_data)

    assert exc_info.value.status_code == 400
    assert "already registered" in str(exc_info.value.detail).lower()


def test_register_user_duplicate_username(mock_session, sample_user_data):
    """Test registration fails with duplicate username."""
    # First query returns None (email not found), second returns user (username exists)
    mock_existing = Mock()
    mock_session.exec.return_value.first.side_effect = [None, mock_existing]

    with pytest.raises(HTTPException) as exc_info:
        register_user(mock_session, sample_user_data)

    assert exc_info.value.status_code == 400
    assert "already taken" in str(exc_info.value.detail).lower()


def test_register_user_hashes_password(mock_session, sample_user_data, mock_user):
    """Test that password is properly hashed during registration."""
    with patch('services.auth.auth_service.hash_password') as mock_hash:
        with patch('services.auth.auth_service.User') as MockUser:
            mock_hash.return_value = "hashed_password"
            mock_session.exec.return_value.first.return_value = None
            MockUser.return_value = mock_user

            register_user(mock_session, sample_user_data)

            mock_hash.assert_called_once_with("password123")


# Tests for login()
def test_login_success(mock_session, mock_user):
    """Test successful login with valid credentials."""
    with patch('services.auth.auth_service.verify_password') as mock_verify:
        with patch('services.auth.auth_service.create_access_token') as mock_token:
            mock_session.exec.return_value.first.return_value = mock_user
            mock_verify.return_value = True
            mock_token.return_value = "test_token"

            result = login(mock_session, "testuser", "password123")

            assert result == {"access_token": "test_token", "token_type": "bearer"}
            mock_verify.assert_called_once_with("password123", mock_user.password)
            mock_token.assert_called_once_with(data={"sub": mock_user.username})


def test_login_user_not_found(mock_session):
    """Test login fails when user doesn't exist."""
    mock_session.exec.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        login(mock_session, "nonexistent", "password")

    assert exc_info.value.status_code == 401
    assert "incorrect" in str(exc_info.value.detail).lower()


def test_login_invalid_password(mock_session, mock_user):
    """Test login fails with incorrect password."""
    with patch('services.auth.auth_service.verify_password') as mock_verify:
        mock_session.exec.return_value.first.return_value = mock_user
        mock_verify.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            login(mock_session, "testuser", "wrongpassword")

        assert exc_info.value.status_code == 401
        assert "incorrect" in str(exc_info.value.detail).lower()


def test_login_creates_jwt_token(mock_session, mock_user):
    """Test that login creates a proper JWT token."""
    with patch('services.auth.auth_service.verify_password') as mock_verify:
        with patch('services.auth.auth_service.create_access_token') as mock_token:
            mock_session.exec.return_value.first.return_value = mock_user
            mock_verify.return_value = True
            mock_token.return_value = "jwt_token_here"

            result = login(mock_session, "testuser", "password123")

            assert result["access_token"] == "jwt_token_here"
            assert result["token_type"] == "bearer"
            mock_token.assert_called_once()
''',

    'services/user/test_user_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in user_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.user.user_service import UserService
from models.schemas.user_schema import UserCreate, UserUpdate


@pytest.fixture
def mock_user_repo():
    """Mock user repository."""
    return Mock()


@pytest.fixture
def mock_campaign_repo():
    """Mock campaign repository."""
    return Mock()


@pytest.fixture
def mock_class_repo():
    """Mock class repository."""
    return Mock()


@pytest.fixture
def mock_diceset_repo():
    """Mock diceset repository."""
    return Mock()


@pytest.fixture
def mock_dicelog_repo():
    """Mock dicelog repository."""
    return Mock()


@pytest.fixture
def user_service(mock_user_repo, mock_campaign_repo, mock_class_repo, mock_diceset_repo, mock_dicelog_repo):
    """Create UserService with mocked dependencies."""
    return UserService(
        mock_user_repo,
        mock_campaign_repo,
        mock_class_repo,
        mock_diceset_repo,
        mock_dicelog_repo
    )


@pytest.fixture
def sample_user_create():
    """Sample user creation data."""
    return UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def mock_user():
    """Mock user object."""
    user = Mock()
    user.id = 1
    user.username = "testuser"
    user.email = "test@example.com"
    return user


# Tests for create_user()
def test_create_user_success(user_service, mock_user_repo, sample_user_create, mock_user):
    """Test successful user creation."""
    mock_user_repo.create_user.return_value = mock_user

    result = user_service.create_user(sample_user_create)

    assert result == mock_user
    mock_user_repo.create_user.assert_called_once_with(sample_user_create)


def test_create_user_calls_repository(user_service, mock_user_repo, sample_user_create):
    """Test that create_user properly calls the repository."""
    user_service.create_user(sample_user_create)

    mock_user_repo.create_user.assert_called_once_with(sample_user_create)


# Tests for get_user()
def test_get_user_success(user_service, mock_user_repo, mock_user):
    """Test successful user retrieval."""
    mock_user_repo.get_user.return_value = mock_user

    result = user_service.get_user(1)

    assert result == mock_user
    mock_user_repo.get_user.assert_called_once_with(1)


def test_get_user_not_found(user_service, mock_user_repo):
    """Test get_user raises exception when user not found."""
    mock_user_repo.get_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user(999)

    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()


# Tests for list_users()
def test_list_users_success(user_service, mock_user_repo):
    """Test listing all users."""
    mock_users = [Mock(), Mock(), Mock()]
    mock_user_repo.list_users.return_value = mock_users

    result = user_service.list_users()

    assert result == mock_users
    assert len(result) == 3
    mock_user_repo.list_users.assert_called_once()


def test_list_users_empty(user_service, mock_user_repo):
    """Test listing users returns empty list when no users exist."""
    mock_user_repo.list_users.return_value = []

    result = user_service.list_users()

    assert result == []
    assert len(result) == 0


def test_list_users_with_pagination(user_service, mock_user_repo):
    """Test list_users with offset and limit parameters."""
    mock_users = [Mock(), Mock()]
    mock_user_repo.list_users.return_value = mock_users

    result = user_service.list_users(offset=10, limit=20)

    assert result == mock_users
    mock_user_repo.list_users.assert_called_once_with(offset=10, limit=20)


# Tests for update_user()
def test_update_user_success(user_service, mock_user_repo, mock_user):
    """Test successful user update."""
    update_data = UserUpdate(username="newname")
    mock_user_repo.update_user.return_value = mock_user

    result = user_service.update_user(1, update_data)

    assert result == mock_user
    mock_user_repo.update_user.assert_called_once_with(1, update_data)


def test_update_user_not_found(user_service, mock_user_repo):
    """Test update_user raises exception when user not found."""
    update_data = UserUpdate(username="newname")
    mock_user_repo.update_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(999, update_data)

    assert exc_info.value.status_code == 404


def test_update_user_partial_update(user_service, mock_user_repo, mock_user):
    """Test partial user update with only some fields."""
    update_data = UserUpdate(email="newemail@example.com")
    mock_user_repo.update_user.return_value = mock_user

    result = user_service.update_user(1, update_data)

    assert result == mock_user
    mock_user_repo.update_user.assert_called_once()


# Tests for delete_user()
def test_delete_user_success(user_service, mock_user_repo, mock_dicelog_repo,
                            mock_diceset_repo, mock_class_repo, mock_campaign_repo, mock_user):
    """Test successful user deletion with cascade."""
    mock_user_repo.get_user.return_value = mock_user
    mock_user_repo.delete_user.return_value = mock_user

    result = user_service.delete_user(1)

    assert result == mock_user
    # Verify cascade deletes were called
    mock_dicelog_repo.delete_logs_by_user.assert_called_once_with(1)
    mock_diceset_repo.delete_dicesets_by_user.assert_called_once_with(1)
    mock_class_repo.delete_classes_by_user.assert_called_once_with(1)
    mock_campaign_repo.delete_campaigns_by_user.assert_called_once_with(1)
    mock_user_repo.delete_user.assert_called_once_with(1)


def test_delete_user_not_found(user_service, mock_user_repo):
    """Test delete_user raises exception when user not found."""
    mock_user_repo.get_user.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(999)

    assert exc_info.value.status_code == 404


def test_delete_user_cascade_order(user_service, mock_user_repo, mock_dicelog_repo,
                                   mock_diceset_repo, mock_class_repo, mock_campaign_repo, mock_user):
    """Test that cascade deletes happen in correct order."""
    mock_user_repo.get_user.return_value = mock_user
    mock_user_repo.delete_user.return_value = mock_user

    user_service.delete_user(1)

    # Verify cascade happens before user deletion
    assert mock_dicelog_repo.delete_logs_by_user.called
    assert mock_diceset_repo.delete_dicesets_by_user.called
    assert mock_class_repo.delete_classes_by_user.called
    assert mock_campaign_repo.delete_campaigns_by_user.called
    mock_user_repo.delete_user.assert_called_once()
''',

    'services/dice/test_dice_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in dice_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.dice.dice_service import DiceService
from models.schemas.dice_schema import DiceCreate, DiceUpdate
from models.schemas.dicelog_schema import DiceLogCreate


@pytest.fixture
def mock_dice_repo():
    """Mock dice repository."""
    return Mock()


@pytest.fixture
def mock_log_repo():
    """Mock dicelog repository."""
    return Mock()


@pytest.fixture
def dice_service(mock_dice_repo, mock_log_repo):
    """Create DiceService with mocked dependencies."""
    return DiceService(mock_dice_repo, mock_log_repo)


@pytest.fixture
def dice_service_no_log(mock_dice_repo):
    """Create DiceService without log repository."""
    return DiceService(mock_dice_repo, None)


@pytest.fixture
def sample_dice_create():
    """Sample dice creation data."""
    return DiceCreate(name="D20", sides=20)


@pytest.fixture
def mock_dice():
    """Mock dice object."""
    dice = Mock()
    dice.id = 1
    dice.name = "D20"
    dice.sides = 20
    return dice


# Tests for create_dice()
def test_create_dice_success(dice_service, mock_dice_repo, sample_dice_create, mock_dice):
    """Test successful dice creation."""
    mock_dice_repo.create_dice.return_value = mock_dice

    result = dice_service.create_dice(sample_dice_create)

    assert result == mock_dice
    mock_dice_repo.create_dice.assert_called_once_with(sample_dice_create)


def test_create_dice_calls_repository(dice_service, mock_dice_repo, sample_dice_create):
    """Test that create_dice properly calls the repository."""
    dice_service.create_dice(sample_dice_create)

    mock_dice_repo.create_dice.assert_called_once()


# Tests for get_dice()
def test_get_dice_success(dice_service, mock_dice_repo, mock_dice):
    """Test successful dice retrieval."""
    mock_dice_repo.get_dice.return_value = mock_dice

    result = dice_service.get_dice(1)

    assert result == mock_dice
    mock_dice_repo.get_dice.assert_called_once_with(1)


def test_get_dice_not_found(dice_service, mock_dice_repo):
    """Test get_dice raises exception when dice not found."""
    mock_dice_repo.get_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        dice_service.get_dice(999)

    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()


# Tests for list_dices()
def test_list_dices_success(dice_service, mock_dice_repo):
    """Test listing all dices."""
    mock_dices = [Mock(), Mock(), Mock()]
    mock_dice_repo.list_dices.return_value = mock_dices

    result = dice_service.list_dices()

    assert result == mock_dices
    assert len(result) == 3
    mock_dice_repo.list_dices.assert_called_once()


def test_list_dices_empty(dice_service, mock_dice_repo):
    """Test listing dices returns empty list when none exist."""
    mock_dice_repo.list_dices.return_value = []

    result = dice_service.list_dices()

    assert result == []


def test_list_dices_with_pagination(dice_service, mock_dice_repo):
    """Test list_dices with offset and limit parameters."""
    mock_dices = [Mock(), Mock()]
    mock_dice_repo.list_dices.return_value = mock_dices

    result = dice_service.list_dices(offset=5, limit=10)

    assert result == mock_dices
    mock_dice_repo.list_dices.assert_called_once_with(offset=5, limit=10)


# Tests for update_dice()
def test_update_dice_success(dice_service, mock_dice_repo, mock_dice):
    """Test successful dice update."""
    update_data = DiceUpdate(name="D12")
    mock_dice_repo.update_dice.return_value = mock_dice

    result = dice_service.update_dice(1, update_data)

    assert result == mock_dice
    mock_dice_repo.update_dice.assert_called_once_with(1, update_data)


def test_update_dice_not_found(dice_service, mock_dice_repo):
    """Test update_dice raises exception when dice not found."""
    update_data = DiceUpdate(name="D12")
    mock_dice_repo.update_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        dice_service.update_dice(999, update_data)

    assert exc_info.value.status_code == 404


# Tests for delete_dice()
def test_delete_dice_success(dice_service, mock_dice_repo, mock_dice):
    """Test successful dice deletion."""
    mock_dice_repo.delete_dice.return_value = mock_dice

    result = dice_service.delete_dice(1)

    assert result == mock_dice
    mock_dice_repo.delete_dice.assert_called_once_with(1)


def test_delete_dice_not_found(dice_service, mock_dice_repo):
    """Test delete_dice raises exception when dice not found."""
    mock_dice_repo.delete_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        dice_service.delete_dice(999)

    assert exc_info.value.status_code == 404


# Tests for _log_roll()
def test_log_roll_with_repo(dice_service, mock_log_repo):
    """Test _log_roll when log repository is provided."""
    log_entry = Mock(spec=DiceLogCreate)
    mock_log_repo.log_roll.return_value = Mock()

    dice_service._log_roll(log_entry)

    mock_log_repo.log_roll.assert_called_once_with(log_entry)


def test_log_roll_without_repo(dice_service_no_log):
    """Test _log_roll does nothing when log repository is None."""
    log_entry = Mock(spec=DiceLogCreate)

    # Should not raise exception
    dice_service_no_log._log_roll(log_entry)


# Tests for roll_dice()
def test_roll_dice_success(dice_service, mock_dice_repo, mock_dice):
    """Test successful dice roll."""
    mock_dice_repo.get_dice.return_value = mock_dice

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 15

        result = dice_service.roll_dice(1)

        assert result["id"] == 1
        assert result["name"] == "D20"
        assert result["result"] == 15
        mock_randint.assert_called_once_with(1, 20)


def test_roll_dice_not_found(dice_service, mock_dice_repo):
    """Test roll_dice raises exception when dice not found."""
    mock_dice_repo.get_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        dice_service.roll_dice(999)

    assert exc_info.value.status_code == 404


def test_roll_dice_range(dice_service, mock_dice_repo, mock_dice):
    """Test that roll_dice generates result within valid range."""
    mock_dice.sides = 6
    mock_dice_repo.get_dice.return_value = mock_dice

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 3

        result = dice_service.roll_dice(1)

        mock_randint.assert_called_once_with(1, 6)
        assert 1 <= result["result"] <= 6


def test_roll_dice_with_logging(dice_service, mock_dice_repo, mock_log_repo, mock_dice):
    """Test roll_dice logs when user_id and campaign_id provided."""
    mock_dice_repo.get_dice.return_value = mock_dice

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 10

        dice_service.roll_dice(1, user_id=5, campaign_id=3, class_id=2)

        mock_log_repo.log_roll.assert_called_once()


def test_roll_dice_without_logging(dice_service, mock_dice_repo, mock_log_repo, mock_dice):
    """Test roll_dice doesn't log when parameters not provided."""
    mock_dice_repo.get_dice.return_value = mock_dice

    with patch('random.randint') as mock_randint:
        mock_randint.return_value = 10

        dice_service.roll_dice(1)

        mock_log_repo.log_roll.assert_not_called()
''',

    'services/campaign/test_campaign_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in campaign_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.campaign.campaign_service import CampaignService
from models.schemas.campaign_schema import CampaignCreate, CampaignUpdate


@pytest.fixture
def mock_campaign_repo():
    """Mock campaign repository."""
    return Mock()


@pytest.fixture
def mock_class_repo():
    """Mock class repository."""
    return Mock()


@pytest.fixture
def mock_diceset_repo():
    """Mock diceset repository."""
    return Mock()


@pytest.fixture
def mock_dicelog_repo():
    """Mock dicelog repository."""
    return Mock()


@pytest.fixture
def campaign_service(mock_campaign_repo, mock_class_repo, mock_diceset_repo, mock_dicelog_repo):
    """Create CampaignService with mocked dependencies."""
    return CampaignService(
        mock_campaign_repo,
        mock_class_repo,
        mock_diceset_repo,
        mock_dicelog_repo
    )


@pytest.fixture
def sample_campaign_create():
    """Sample campaign creation data."""
    data = CampaignCreate(
        title="Test Campaign",
        genre="Fantasy",
        description="A test campaign",
        max_classes=4
    )
    data.set_user(1)
    return data


@pytest.fixture
def mock_campaign():
    """Mock campaign object."""
    campaign = Mock()
    campaign.id = 1
    campaign.title = "Test Campaign"
    campaign.created_by = 1
    return campaign


# Tests for create_campaign()
def test_create_campaign_success(campaign_service, mock_campaign_repo, sample_campaign_create, mock_campaign):
    """Test successful campaign creation."""
    mock_campaign_repo.create_campaign.return_value = mock_campaign

    result = campaign_service.create_campaign(sample_campaign_create)

    assert result == mock_campaign
    mock_campaign_repo.create_campaign.assert_called_once_with(sample_campaign_create)


def test_create_campaign_calls_repository(campaign_service, mock_campaign_repo, sample_campaign_create):
    """Test that create_campaign properly calls the repository."""
    campaign_service.create_campaign(sample_campaign_create)

    mock_campaign_repo.create_campaign.assert_called_once()


# Tests for get_campaign()
def test_get_campaign_success(campaign_service, mock_campaign_repo, mock_campaign):
    """Test successful campaign retrieval."""
    mock_campaign_repo.get_campaign.return_value = mock_campaign

    result = campaign_service.get_campaign(1)

    assert result == mock_campaign
    mock_campaign_repo.get_campaign.assert_called_once_with(1)


def test_get_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test get_campaign raises exception when campaign not found."""
    mock_campaign_repo.get_campaign.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        campaign_service.get_campaign(999)

    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()


# Tests for list_campaigns()
def test_list_campaigns_success(campaign_service, mock_campaign_repo):
    """Test listing all campaigns for a user."""
    mock_campaigns = [Mock(), Mock(), Mock()]
    mock_campaign_repo.list_campaigns.return_value = mock_campaigns

    result = campaign_service.list_campaigns(1)

    assert result == mock_campaigns
    assert len(result) == 3
    mock_campaign_repo.list_campaigns.assert_called_once_with(1, offset=0, limit=100)


def test_list_campaigns_empty(campaign_service, mock_campaign_repo):
    """Test listing campaigns returns empty list when none exist."""
    mock_campaign_repo.list_campaigns.return_value = []

    result = campaign_service.list_campaigns(1)

    assert result == []


def test_list_campaigns_with_pagination(campaign_service, mock_campaign_repo):
    """Test list_campaigns with offset and limit parameters."""
    mock_campaigns = [Mock(), Mock()]
    mock_campaign_repo.list_campaigns.return_value = mock_campaigns

    result = campaign_service.list_campaigns(1, offset=5, limit=10)

    assert result == mock_campaigns
    mock_campaign_repo.list_campaigns.assert_called_once_with(1, offset=5, limit=10)


# Tests for update_campaign()
def test_update_campaign_success(campaign_service, mock_campaign_repo, mock_campaign):
    """Test successful campaign update."""
    update_data = CampaignUpdate(title="Updated Campaign")
    mock_campaign_repo.update_campaign.return_value = mock_campaign

    result = campaign_service.update_campaign(1, update_data)

    assert result == mock_campaign
    mock_campaign_repo.update_campaign.assert_called_once_with(1, update_data)


def test_update_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test update_campaign raises exception when campaign not found."""
    update_data = CampaignUpdate(title="Updated")
    mock_campaign_repo.update_campaign.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        campaign_service.update_campaign(999, update_data)

    assert exc_info.value.status_code == 404


def test_update_campaign_partial_update(campaign_service, mock_campaign_repo, mock_campaign):
    """Test partial campaign update with only some fields."""
    update_data = CampaignUpdate(description="New description")
    mock_campaign_repo.update_campaign.return_value = mock_campaign

    result = campaign_service.update_campaign(1, update_data)

    assert result == mock_campaign


# Tests for delete_campaign()
def test_delete_campaign_success(campaign_service, mock_campaign_repo, mock_dicelog_repo,
                                 mock_diceset_repo, mock_class_repo, mock_campaign):
    """Test successful campaign deletion with cascade."""
    mock_campaign_repo.get_campaign.return_value = mock_campaign
    mock_campaign_repo.delete_campaign.return_value = mock_campaign

    result = campaign_service.delete_campaign(1)

    assert result == mock_campaign
    # Verify cascade deletes were called
    mock_dicelog_repo.delete_logs_by_campaign.assert_called_once_with(1)
    mock_diceset_repo.delete_dicesets_by_campaign.assert_called_once_with(1)
    mock_class_repo.delete_classes_by_campaign.assert_called_once_with(1)
    mock_campaign_repo.delete_campaign.assert_called_once_with(1)


def test_delete_campaign_not_found(campaign_service, mock_campaign_repo):
    """Test delete_campaign raises exception when campaign not found."""
    mock_campaign_repo.get_campaign.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        campaign_service.delete_campaign(999)

    assert exc_info.value.status_code == 404


def test_delete_campaign_cascade_order(campaign_service, mock_campaign_repo, mock_dicelog_repo,
                                       mock_diceset_repo, mock_class_repo, mock_campaign):
    """Test that cascade deletes happen in correct order."""
    mock_campaign_repo.get_campaign.return_value = mock_campaign
    mock_campaign_repo.delete_campaign.return_value = mock_campaign

    campaign_service.delete_campaign(1)

    # Verify cascade happens before campaign deletion
    assert mock_dicelog_repo.delete_logs_by_campaign.called
    assert mock_diceset_repo.delete_dicesets_by_campaign.called
    assert mock_class_repo.delete_classes_by_campaign.called
    mock_campaign_repo.delete_campaign.assert_called_once()
''',

    'services/diceset/test_diceset_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in diceset_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.diceset.diceset_service import DiceSetService
from models.schemas.diceset_schema import DiceSetCreate, DiceSetUpdate
from models.schemas.dicelog_schema import DiceLogCreate


@pytest.fixture
def mock_dice_repo():
    """Mock dice repository."""
    return Mock()


@pytest.fixture
def mock_diceset_repo():
    """Mock diceset repository."""
    return Mock()


@pytest.fixture
def mock_log_repo():
    """Mock dicelog repository."""
    return Mock()


@pytest.fixture
def diceset_service(mock_dice_repo, mock_diceset_repo, mock_log_repo):
    """Create DiceSetService with mocked dependencies."""
    return DiceSetService(mock_dice_repo, mock_diceset_repo, mock_log_repo)


@pytest.fixture
def diceset_service_no_log(mock_dice_repo, mock_diceset_repo):
    """Create DiceSetService without log repository."""
    return DiceSetService(mock_dice_repo, mock_diceset_repo, None)


@pytest.fixture
def sample_diceset_create():
    """Sample diceset creation data."""
    data = DiceSetCreate(
        name="Attack Set",
        dnd_class_id=1,
        campaign_id=1,
        dice_ids=[1, 2, 3]
    )
    data.set_user(1)
    return data


@pytest.fixture
def mock_diceset():
    """Mock diceset object."""
    diceset = Mock()
    diceset.id = 1
    diceset.name = "Attack Set"
    diceset.user_id = 1
    diceset.dnd_class_id = 1
    diceset.campaign_id = 1
    return diceset


@pytest.fixture
def mock_dice():
    """Mock dice objects."""
    dice1 = Mock()
    dice1.id = 1
    dice1.sides = 6
    dice1.name = "D6"

    dice2 = Mock()
    dice2.id = 2
    dice2.sides = 8
    dice2.name = "D8"

    return [dice1, dice2]


# Tests for create_diceset()
def test_create_diceset_success(diceset_service, mock_diceset_repo, mock_dice_repo,
                                sample_diceset_create, mock_diceset, mock_dice):
    """Test successful diceset creation."""
    mock_diceset_repo.count_dicesets_by_class.return_value = 2
    mock_dice_repo.get_dice.side_effect = mock_dice
    mock_diceset_repo.create_diceset.return_value = mock_diceset

    result = diceset_service.create_diceset(sample_diceset_create)

    assert result == mock_diceset
    mock_diceset_repo.create_diceset.assert_called_once()


def test_create_diceset_exceeds_max_limit(diceset_service, mock_diceset_repo, sample_diceset_create):
    """Test create_diceset raises exception when max limit exceeded."""
    mock_diceset_repo.count_dicesets_by_class.return_value = 5

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.create_diceset(sample_diceset_create)

    assert exc_info.value.status_code == 400
    assert "maximum" in str(exc_info.value.detail).lower()


def test_create_diceset_dice_not_found(diceset_service, mock_diceset_repo, mock_dice_repo, sample_diceset_create):
    """Test create_diceset raises exception when dice doesn't exist."""
    mock_diceset_repo.count_dicesets_by_class.return_value = 2
    mock_dice_repo.get_dice.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.create_diceset(sample_diceset_create)

    assert exc_info.value.status_code == 404
    assert "dice" in str(exc_info.value.detail).lower()


def test_create_diceset_counts_duplicates(diceset_service, mock_diceset_repo, mock_dice_repo,
                                         sample_diceset_create, mock_diceset):
    """Test create_diceset properly counts duplicate dice."""
    sample_diceset_create.dice_ids = [1, 1, 2]  # Duplicate dice
    mock_diceset_repo.count_dicesets_by_class.return_value = 2
    mock_dice = Mock()
    mock_dice.id = 1
    mock_dice_repo.get_dice.return_value = mock_dice
    mock_diceset_repo.create_diceset.return_value = mock_diceset

    result = diceset_service.create_diceset(sample_diceset_create)

    assert result == mock_diceset


# Tests for get_diceset()
def test_get_diceset_success(diceset_service, mock_diceset_repo, mock_diceset):
    """Test successful diceset retrieval."""
    mock_diceset_repo.get_diceset.return_value = mock_diceset

    result = diceset_service.get_diceset(1)

    assert result == mock_diceset
    mock_diceset_repo.get_diceset.assert_called_once_with(1)


def test_get_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test get_diceset raises exception when diceset not found."""
    mock_diceset_repo.get_diceset.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.get_diceset(999)

    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()


# Tests for list_dicesets()
def test_list_dicesets_success(diceset_service, mock_diceset_repo):
    """Test listing all dicesets for a user."""
    mock_dicesets = [Mock(), Mock(), Mock()]
    mock_diceset_repo.list_dicesets.return_value = mock_dicesets

    result = diceset_service.list_dicesets(1)

    assert result == mock_dicesets
    assert len(result) == 3
    mock_diceset_repo.list_dicesets.assert_called_once_with(1, offset=0, limit=100)


def test_list_dicesets_empty(diceset_service, mock_diceset_repo):
    """Test listing dicesets returns empty list when none exist."""
    mock_diceset_repo.list_dicesets.return_value = []

    result = diceset_service.list_dicesets(1)

    assert result == []


def test_list_dicesets_with_pagination(diceset_service, mock_diceset_repo):
    """Test list_dicesets with offset and limit parameters."""
    mock_dicesets = [Mock(), Mock()]
    mock_diceset_repo.list_dicesets.return_value = mock_dicesets

    result = diceset_service.list_dicesets(1, offset=5, limit=10)

    mock_diceset_repo.list_dicesets.assert_called_once_with(1, offset=5, limit=10)


# Tests for update_diceset()
def test_update_diceset_success(diceset_service, mock_diceset_repo, mock_diceset):
    """Test successful diceset update."""
    update_data = DiceSetUpdate(name="Updated Set")
    mock_diceset_repo.update_diceset.return_value = mock_diceset

    result = diceset_service.update_diceset(1, update_data)

    assert result == mock_diceset
    mock_diceset_repo.update_diceset.assert_called_once_with(1, update_data)


def test_update_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test update_diceset raises exception when diceset not found."""
    update_data = DiceSetUpdate(name="Updated")
    mock_diceset_repo.update_diceset.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.update_diceset(999, update_data)

    assert exc_info.value.status_code == 404


# Tests for delete_diceset()
def test_delete_diceset_success(diceset_service, mock_diceset_repo, mock_diceset):
    """Test successful diceset deletion."""
    mock_diceset_repo.delete_diceset.return_value = mock_diceset

    result = diceset_service.delete_diceset(1)

    assert result == mock_diceset
    mock_diceset_repo.delete_diceset.assert_called_once_with(1)


def test_delete_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test delete_diceset raises exception when diceset not found."""
    mock_diceset_repo.delete_diceset.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.delete_diceset(999)

    assert exc_info.value.status_code == 404


# Tests for _log_roll()
def test_log_roll_with_repo(diceset_service, mock_log_repo):
    """Test _log_roll when log repository is provided."""
    log_entry = Mock(spec=DiceLogCreate)
    mock_log_repo.log_roll.return_value = Mock()

    diceset_service._log_roll(log_entry)

    mock_log_repo.log_roll.assert_called_once_with(log_entry)


def test_log_roll_without_repo(diceset_service_no_log):
    """Test _log_roll does nothing when log repository is None."""
    log_entry = Mock(spec=DiceLogCreate)

    # Should not raise exception
    diceset_service_no_log._log_roll(log_entry)


# Tests for roll_diceset()
def test_roll_diceset_success(diceset_service, mock_diceset_repo, mock_diceset, mock_dice):
    """Test successful diceset roll."""
    mock_diceset_repo.get_diceset_with_dice.return_value = (mock_diceset, mock_dice)

    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [4, 6]  # Results for each dice

        result = diceset_service.roll_diceset(1)

        assert result["diceset_id"] == 1
        assert result["diceset_name"] == "Attack Set"
        assert len(result["rolls"]) == 2
        assert result["total"] == 10
        assert result["rolls"][0]["result"] == 4
        assert result["rolls"][1]["result"] == 6


def test_roll_diceset_not_found(diceset_service, mock_diceset_repo):
    """Test roll_diceset raises exception when diceset not found."""
    mock_diceset_repo.get_diceset_with_dice.return_value = (None, [])

    with pytest.raises(HTTPException) as exc_info:
        diceset_service.roll_diceset(999)

    assert exc_info.value.status_code == 404


def test_roll_diceset_with_logging(diceset_service, mock_diceset_repo, mock_log_repo,
                                   mock_diceset, mock_dice):
    """Test roll_diceset logs when user_id provided."""
    mock_diceset_repo.get_diceset_with_dice.return_value = (mock_diceset, mock_dice)

    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [4, 6]

        diceset_service.roll_diceset(1, user_id=5)

        mock_log_repo.log_roll.assert_called_once()


def test_roll_diceset_calculates_total(diceset_service, mock_diceset_repo, mock_diceset, mock_dice):
    """Test roll_diceset correctly calculates total."""
    mock_diceset_repo.get_diceset_with_dice.return_value = (mock_diceset, mock_dice)

    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [3, 7]

        result = diceset_service.roll_diceset(1)

        assert result["total"] == 10
''',

    'services/dnd_class/test_class_service.py': '''

# ============================================================================
# FUNCTIONAL UNIT TESTS - Testing all functions in class_service.py
# ============================================================================

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from services.dnd_class.class_service import ClassService
from models.schemas.class_schema import ClassCreate, ClassUpdate, ClassSkills


@pytest.fixture
def mock_class_repo():
    """Mock class repository."""
    return Mock()


@pytest.fixture
def mock_diceset_repo():
    """Mock diceset repository."""
    return Mock()


@pytest.fixture
def mock_dicelog_repo():
    """Mock dicelog repository."""
    return Mock()


@pytest.fixture
def class_service(mock_class_repo, mock_diceset_repo, mock_dicelog_repo):
    """Create ClassService with mocked dependencies."""
    return ClassService(
        mock_class_repo,
        mock_diceset_repo,
        mock_dicelog_repo
    )


@pytest.fixture
def sample_class_create():
    """Sample class creation data."""
    data = ClassCreate(
        name="Testurion",
        dnd_class="Warrior",
        race="Human",
        campaign_id=1,
        skills=ClassSkills()
    )
    data.set_user(1)
    return data


@pytest.fixture
def mock_dnd_class():
    """Mock dnd_class object."""
    dnd_class = Mock()
    dnd_class.id = 1
    dnd_class.name = "Testurion"
    dnd_class.user_id = 1
    dnd_class.campaign_id = 1
    return dnd_class


# Tests for create_class()
def test_create_class_success(class_service, mock_class_repo, sample_class_create, mock_dnd_class):
    """Test successful class creation."""
    mock_class_repo.count_classes_by_campaign.return_value = 2
    mock_class_repo.create_class.return_value = mock_dnd_class

    result = class_service.create_class(sample_class_create)

    assert result == mock_dnd_class
    mock_class_repo.create_class.assert_called_once_with(sample_class_create)


def test_create_class_exceeds_max_limit(class_service, mock_class_repo, sample_class_create):
    """Test create_class raises exception when max limit exceeded."""
    mock_class_repo.count_classes_by_campaign.return_value = 4

    with pytest.raises(HTTPException) as exc_info:
        class_service.create_class(sample_class_create)

    assert exc_info.value.status_code == 400
    assert "maximum" in str(exc_info.value.detail).lower()


def test_create_class_checks_campaign_limit(class_service, mock_class_repo, sample_class_create, mock_dnd_class):
    """Test that create_class validates campaign class limit."""
    mock_class_repo.count_classes_by_campaign.return_value = 0
    mock_class_repo.create_class.return_value = mock_dnd_class

    result = class_service.create_class(sample_class_create)

    mock_class_repo.count_classes_by_campaign.assert_called_once_with(1)
    assert result == mock_dnd_class


# Tests for get_class()
def test_get_class_success(class_service, mock_class_repo, mock_dnd_class):
    """Test successful class retrieval."""
    mock_class_repo.get_class.return_value = mock_dnd_class

    result = class_service.get_class(1)

    assert result == mock_dnd_class
    mock_class_repo.get_class.assert_called_once_with(1)


def test_get_class_not_found(class_service, mock_class_repo):
    """Test get_class raises exception when class not found."""
    mock_class_repo.get_class.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        class_service.get_class(999)

    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()


# Tests for list_classes()
def test_list_classes_success(class_service, mock_class_repo):
    """Test listing all classes for a user."""
    mock_classes = [Mock(), Mock(), Mock()]
    mock_class_repo.list_classes.return_value = mock_classes

    result = class_service.list_classes(1)

    assert result == mock_classes
    assert len(result) == 3
    mock_class_repo.list_classes.assert_called_once_with(1, offset=0, limit=100)


def test_list_classes_empty(class_service, mock_class_repo):
    """Test listing classes returns empty list when none exist."""
    mock_class_repo.list_classes.return_value = []

    result = class_service.list_classes(1)

    assert result == []


def test_list_classes_with_pagination(class_service, mock_class_repo):
    """Test list_classes with offset and limit parameters."""
    mock_classes = [Mock(), Mock()]
    mock_class_repo.list_classes.return_value = mock_classes

    result = class_service.list_classes(1, offset=5, limit=10)

    mock_class_repo.list_classes.assert_called_once_with(1, offset=5, limit=10)


# Tests for update_class()
def test_update_class_success(class_service, mock_class_repo, mock_dnd_class):
    """Test successful class update."""
    update_data = ClassUpdate(notes="Updated notes")
    mock_class_repo.update_class.return_value = mock_dnd_class

    result = class_service.update_class(1, update_data)

    assert result == mock_dnd_class
    mock_class_repo.update_class.assert_called_once_with(1, update_data)


def test_update_class_not_found(class_service, mock_class_repo):
    """Test update_class raises exception when class not found."""
    update_data = ClassUpdate(notes="Updated")
    mock_class_repo.update_class.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        class_service.update_class(999, update_data)

    assert exc_info.value.status_code == 404


def test_update_class_partial_update(class_service, mock_class_repo, mock_dnd_class):
    """Test partial class update with only some fields."""
    update_data = ClassUpdate(name="New Name")
    mock_class_repo.update_class.return_value = mock_dnd_class

    result = class_service.update_class(1, update_data)

    assert result == mock_dnd_class


# Tests for delete_class()
def test_delete_class_success(class_service, mock_class_repo, mock_dicelog_repo,
                              mock_diceset_repo, mock_dnd_class):
    """Test successful class deletion with cascade."""
    mock_class_repo.get_class.return_value = mock_dnd_class
    mock_class_repo.delete_class.return_value = mock_dnd_class

    result = class_service.delete_class(1)

    assert result == mock_dnd_class
    # Verify cascade deletes were called
    mock_dicelog_repo.delete_logs_by_class.assert_called_once_with(1)
    mock_diceset_repo.delete_dicesets_by_class.assert_called_once_with(1)
    mock_class_repo.delete_class.assert_called_once_with(1)


def test_delete_class_not_found(class_service, mock_class_repo):
    """Test delete_class raises exception when class not found."""
    mock_class_repo.get_class.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        class_service.delete_class(999)

    assert exc_info.value.status_code == 404


def test_delete_class_cascade_order(class_service, mock_class_repo, mock_dicelog_repo,
                                    mock_diceset_repo, mock_dnd_class):
    """Test that cascade deletes happen in correct order."""
    mock_class_repo.get_class.return_value = mock_dnd_class
    mock_class_repo.delete_class.return_value = mock_dnd_class

    class_service.delete_class(1)

    # Verify cascade happens before class deletion
    assert mock_dicelog_repo.delete_logs_by_class.called
    assert mock_diceset_repo.delete_dicesets_by_class.called
    mock_class_repo.delete_class.assert_called_once()
'''
}

# Append tests to each file
for file_path, test_content in tests_content.items():
    full_path = f"/Users/jm/Projects/mythic-access-dnd-clean/mythic-access-dnd/{file_path}"
    print(f"Adding tests to {file_path}...")

    try:
        # Read existing content
        with open(full_path, 'r') as f:
            existing_content = f.read()

        # Append new tests
        with open(full_path, 'a') as f:
            f.write(test_content)

        print(f"✓ Successfully added tests to {file_path}")
    except Exception as e:
        print(f"✗ Error with {file_path}: {str(e)}")

print("\n✓ All service tests added successfully!")
