"""
test_db.py

Creates a fake database SQLite for unit tests.
"""
import os
from sqlmodel import SQLModel, create_engine, Session
from models.db_models.table_models import (
    User,
    Campaign,
    Class,
    Dice,
    DiceSet,
    DiceLog
)



# Remove old test DB file so tests start with a clean DB
TEST_DB_PATH = "./models/db_models/test.db.sql"
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

# Engine for file-based sqlite test DB
test_engine = create_engine(
    f"sqlite:///{TEST_DB_PATH}",
    connect_args={"check_same_thread": False},
    pool_size=20,
    max_overflow=20,
    pool_timeout=20
)


# Drop & recreate all tables once at the start
SQLModel.metadata.drop_all(test_engine)
SQLModel.metadata.create_all(test_engine)


# Helper: create session
def get_session():
    """Create a db session for test (SQLite file)."""
    with Session(test_engine) as session:
        yield session
