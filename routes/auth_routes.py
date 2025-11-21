"""
auth_routes.py

API endpoints to handle authentication operations.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from rate_limit import limiter
from sqlmodel import Session
from models.schemas.user_schema import UserCreate, UserMe, UserPublic
from models.schemas.auth_schema import Token
from auth.auth import get_current_user
from dependencies import get_session
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()


@router.post("/register", response_model=UserPublic)
@limiter.limit("3/minute")
def register_user(
        request: Request,
        user_data: UserCreate,
        session: Session = Depends(get_session)):
    """Endpoint to register a new user."""
    db_user = auth_service.register_user(session, user_data)
    return UserPublic(
        id=db_user.id,
        user_name=db_user.user_name,
        created_at=db_user.created_at
    )


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login_for_access_token(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """Endpoint to authenticate a user via login."""
    return auth_service.login(
        session=session,
        login=form_data.username,
        password=form_data.password
    )


@router.get("/me", response_model=UserMe)
@limiter.limit("30/minute")
def get_my_profile(
        request: Request,
        current_user = Depends(get_current_user)
):
    """Returns the authenticated users info."""
    return UserMe.model_validate(current_user)
