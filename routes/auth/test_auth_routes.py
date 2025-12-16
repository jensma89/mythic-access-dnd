# """
# test_auth_routes.py
# 
# Test the auth endpoints for register/login and users/me.
# """
# from fastapi.testclient import TestClient
# 
# from main import app
# from dependencies import get_session as prod_get_session
# from models.db_models.test_db import get_session as get_test_session
# from models.db_models.test_db import test_engine
# from sqlmodel import Session
# from auth.test_helpers import create_test_user, get_test_token
# 
# # Override the DB dependency for tests
# app.dependency_overrides[prod_get_session] = get_test_session
# 
# 
# # Success tests
# 
# def test_register():
#     """Test user registration using the test DB."""
#     session = Session(test_engine)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/register",
#         json={
#             "user_name": "newtester",
#             "email": "newtester@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["user_name"] == "newtester"
#     assert "id" in data
#     assert "created_at" in data
# 
# 
# def test_login():
#     """Test the user login using the test DB."""
#     # Use test session
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": test_user.email,
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 200
# 
#     json_resp = response.json()
#     assert "access_token" in json_resp
#     assert "token_type" in json_resp
# 
# 
# def test_me():
#     """Test the /auth/me endpoint."""
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     token = get_test_token(test_user)
# 
#     auth_client = TestClient(app)
#     auth_client.headers = {"Authorization": f"Bearer {token}"}
# 
#     response = auth_client.get("/auth/me")
# 
#     assert response.status_code == 200
# 
#     data = response.json()
#     assert data["id"] == test_user.id
#     assert data["user_name"] == test_user.user_name
#     assert data["email"] == test_user.email
# # Error tests
# 
# def test_register_duplicate_email():
#     """Registering the same email twice."""
#     session = Session(test_engine)
#     client = TestClient(app)
# 
#     # First user (normal)
#     client.post(
#         "/auth/register",
#         json={
#             "user_name": "dup",
#             "email": "dup@example.com",
#             "password": "password123"
#         }
#     )
# 
#     # Second user → expect failure
#     response = client.post(
#         "/auth/register",
#         json={
#             "user_name": "dup2",
#             "email": "dup@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 400
# 
# 
# def test_login_wrong_password():
#     """Login with incorrect password."""
#     session = Session(test_engine)
#     test_user = create_test_user(session)
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": test_user.email,
#             "password": "WRONGPASS"
#         }
#     )
# 
#     assert response.status_code == 401
# 
# 
# def test_login_user_not_found():
#     """Login with non existen email."""
#     client = TestClient(app)
# 
#     response = client.post(
#         "/auth/login",
#         data={
#             "username": "idontexist@example.com",
#             "password": "password123"
#         }
#     )
# 
#     assert response.status_code == 401
# 
# 
# def test_me_unauthorized():
#     """Calling /me without a token."""
#     client = TestClient(app)
# 
#     response = client.get("/auth/me")
# 
#     assert response.status_code == 401
