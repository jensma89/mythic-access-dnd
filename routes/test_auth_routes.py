from fastapi.testclient import TestClient
from main import app
from dependencies import get_session
from models.db_models.test_db import get_session as get_test_session
from auth.test_helpers import create_test_user
from services.auth_service import AuthService

# Override the DB dependency for tests
app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

def test_login():
    """Test the user login using the test DB."""
    # Use test session
    session = next(get_test_session())
    test_user = create_test_user(session)

    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    json_resp = response.json()
    assert "access_token" in json_resp
    assert "token_type" in json_resp
