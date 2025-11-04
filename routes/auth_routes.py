"""
auth_routes.py

"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session, select
from models.db_models.table_models import User
from models.schemas.user_schema import UserCreate, UserMe, UserPublic
from models.schemas.auth_schema import Token
from auth.auth import *
from dependencies import SessionDep


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserPublic)
def register_user(
        user_data: UserCreate,
        session: Session = Depends(SessionDep)):
    """Register a new user.
    Check for duplicate email or username.
    Hashes password."""
    # Check for existing username or email
    existing = session.exec(
        select(User)
        .where((User.email == user_data.email)
               | User.user_name == user_data.user_name)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A user with that email or username already exists."
        )

    db_user = User(
        user_name=user_data.user_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserPublic.model_validate(db_user)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(SessionDep)
):
    """Login a user and issue a JWT access token."""
    user = await authenticate_user(
        session,
        email=form_data.username,
        password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserMe)
async def get_my_profile(
        current_user: User = Depends(get_current_user)):
    """Returns the authenticated users info."""
    return UserMe.model_validate(current_user)
