# models/db_models/test_db.py

import os
from sqlmodel import SQLModel, create_engine, Session



# Remove old test DB file so tests start with a clean DB
TEST_DB_PATH = "./test.db.sql"
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

# Engine for file-based sqlite test DB
engine = create_engine(
    f"sqlite:///{TEST_DB_PATH}",
    connect_args={"check_same_thread": False}
)

# Create tables
SQLModel.metadata.create_all(engine)

# Helper: create session
def get_session():
    """Create a db session for test (SQLite file)."""
    with Session(engine) as session:
        yield session
