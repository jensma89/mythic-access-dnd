"""
dependencies.py

DB-Session, Config...
"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_session():
    """Get a database session and close it"""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]