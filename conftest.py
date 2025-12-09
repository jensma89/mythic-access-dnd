"""
conftest.py

Pytest configuration - sets environment variables before any imports.
"""
import os
import sys
from pathlib import Path

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
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user, get_test_token
from main import app
from dependencies import get_session as prod_get_session

# Override the DB dependency for tests
app.dependency_overrides[prod_get_session] = get_test_session


def get_db_session():
    """Get a test database session with proper cleanup."""
    gen = get_test_session()
    session = next(gen)
    try:
        yield session
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


def get_test_user():
    """Create and return a test user with isolated session."""
    session = next(get_test_session())
    user = create_test_user(session)
    return user, session


def get_auth_client():
    """
    Get an authenticated test client with a test user.
    Returns: (client, test_user, session)
    """
    session = next(get_test_session())
    test_user = create_test_user(session)
    token = get_test_token(test_user)

    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}

    return client, test_user, session
