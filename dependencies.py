"""
dependencies.py

DB-Session, Config...
"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from services.user_service import UserService
from repositories.sql_user_repository import SqlAlchemyUserRepository
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)



def create_db_and_tables():
    """Create db and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session and close it"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

"""
def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(SqlAlchemyUserRepository(session))
"""
