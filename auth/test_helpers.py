"""
test_helpers.py


"""
from datetime import timedelta
from sqlmodel import Session
import uuid

from models.db_models.table_models import User
from auth.auth import hash_password, create_access_token



def create_test_user(session: Session):
    """Create a test user
    to test endpoints with token."""
    suffix = uuid.uuid4().hex[:8] # Create random id

    test_user = User(
        user_name=f"test_user_{suffix}",
        email=f"test_{suffix}@example.com",
        hashed_password=hash_password("password123")
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user)
    return test_user


def get_test_token(test_user: User):
    """Create a test token for test user."""
    access_token_expires = timedelta(minutes=60)
    token = create_access_token(
        data={"sub": test_user.email},
        expires_delta=access_token_expires
    )
    return token
