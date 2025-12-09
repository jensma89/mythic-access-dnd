"""
conftest.py

Pytest configuration - sets environment variables before any imports.
"""
import os
import sys
from pathlib import Path
from contextlib import contextmanager

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables BEFORE any imports
os.environ['DATABASE_URL'] = 'sqlite:///./models/db_models/test.db.sql'

# ALWAYS set SECRET_KEY if not already set (for tests to work)
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only-do-not-use-in-production'

# Import after environment setup
from fastapi.testclient import TestClient
from models.db_models.test_db import get_session as get_test_session, test_engine
from sqlmodel import Session
from auth.test_helpers import create_test_user, get_test_token
from main import app
from dependencies import get_session as prod_get_session

# Override the DB dependency for tests
app.dependency_overrides[prod_get_session] = get_test_session


@contextmanager
def get_db_session():
    """Get a test database session with automatic cleanup."""
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()


def get_session_for_test():
    """Get a test database session that will be auto-closed."""
    return Session(test_engine)
