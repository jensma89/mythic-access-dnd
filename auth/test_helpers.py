"""
test_helpers.py


"""
from datetime import timedelta
from sqlmodel import Session
import uuid

from models.db_models.table_models import *
from auth.auth import hash_password, create_access_token

from services.campaign.campaign_service import CampaignService
from models.schemas.campaign_schema import CampaignCreate
from repositories.sql_campaign_repository import SqlAlchemyCampaignRepository
from repositories.sql_class_repository import SqlAlchemyClassRepository
from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository



def create_test_user(session: Session) -> User:
    """Create a random test user."""
    suffix = uuid.uuid4().hex[:8]
    user = User(
        user_name=f"test_user_{suffix}",
        email=f"test_{suffix}@example.com",
        hashed_password=hash_password("password123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_test_token(user: User) -> str:
    """Generate a JWT token for a test user."""
    return create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=60)
    )


def create_test_campaign(session: Session, user: User):
    """Create a test campaign with real repositories."""
    payload = CampaignCreate(
        title="Test Campaign",
        genre="Fantasy",
        description="Temporary campaign",
        max_classes=4
    )
    payload.set_user(user.id)

    campaign_repo = SqlAlchemyCampaignRepository(session)
    class_repo = SqlAlchemyClassRepository(session)
    diceset_repo = SqlAlchemyDiceSetRepository(session)

    service = CampaignService(
        campaign_repo,
        class_repo,
        diceset_repo,
        None
    )
    return service.create_campaign(payload)
