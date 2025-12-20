"""
dependencies.py

DB-Session, Config...
"""
from typing import Annotated
from fastapi import Depends, Query
from sqlmodel import create_engine,select, Session, SQLModel
from models.db_models.table_models import Dice
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./models/db_models/test.db.sql"
)

engine = create_engine(DATABASE_URL, echo=False) # Set echo True for debug mode



def create_db_and_tables():
    """Create db and tables with
    the fixed dice table."""
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        dice = [
            Dice(name="d4", sides=4),
            Dice(name="d6", sides=6),
            Dice(name="d8", sides=8),
            Dice(name="d10", sides=10),
            Dice(name="d12", sides=12),
            Dice(name="d20", sides=20),
            Dice(name="d100", sides=100),
        ]

        for d in dice:
            exists = session.exec(
                select(Dice).where(Dice.name == d.name)
            ).first()
            if not exists:
                session.add(d)

        session.commit()


def get_session():
    """Get a database session and close it"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class Pagination:
    """Pagination parameters for endpoints."""
    def __init__(
            self,
            offset: Annotated[int, Query(ge=0)] = 0,
            limit: Annotated[int, Query(le=100)] = 100
    ):
        self.offset = offset
        self.limit = limit


# Query parameter classes

class UserQueryParams:
    """Optional filters for users."""
    def __init__(
            self,
        name: str | None = Query(
            None,
            description="Filter by username.")):
        self.name = name


class CampaignQueryParams:
    """Optional filters for campaigns."""
    def __init__(
            self,
            user_id: int | None = Query(
                None,
                ge=1,
                description="Filter by user ID."),
            name: str | None = Query(
                None,
                description="Filter by campaign title.")):
        self.user_id = user_id
        self.name = name


class ClassQueryParams:
    """Optional filters for dnd classes."""
    def __init__(
            self,
    campaign_id: int | None = Query(
        None,
        ge=1,
        description="Filter by campaign ID."),
    name: str | None = Query(
        None,
        description="Filter by dnd_class name.")):
        self.campaign_id = campaign_id
        self.name = name
