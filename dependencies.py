"""
dependencies.py

DB-Session, Config...
"""
from typing import Annotated
from fastapi import Depends, Query
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False) # Set echo True for debug mode



def create_db_and_tables():
    """Create db and tables"""
    SQLModel.metadata.create_all(engine)


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
