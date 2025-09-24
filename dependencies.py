"""
dependencies.py

DB-Session, Config...
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False) # Create a DB session for API routes


def get_db():
    """Get a Database Session with yield and finally close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
