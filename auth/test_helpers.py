"""
test_helpers.py


"""
from datetime import timedelta
from sqlmodel import Session

from models.db_models.table_models import User
from auth.auth import hash_password, create_access_token



def create_test_user(session: Session):
    """Create a test user
    to test endpoints with token."""
    test_user = User(
        user_name="test_user",
        email="test_user@example.com",
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
