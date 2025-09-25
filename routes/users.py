"""
users.py

The API routes for users
"""
from typing import List, Annotated
from fastapi import APIRouter, Depends,HTTPException, Query
from sqlmodel import select
from models.db_models.table_models import User
from models.schemas.user_schema import *
from dependencies import SessionDep


router = APIRouter(tags=["users"])


@router.get("/users/", response_model=List[UserPublic])
async def read_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
        users = (
            session.exec(select(User)
                         .offset(offset)
                         .limit(limit)).all())
        return users


@router.post("/users/", response_model=UserPublic)
async def add_user(user: UserCreate, session: SessionDep):
    # New User object
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        hashed_password=user.hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put("/users/{user_id}", response_model=UserPublic)
async def update_user(
        user_id: int,
        user: UserUpdate,
        session: SessionDep
):
    # Get user from DB
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only the fields that are changed by client
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", response_model=UserPublic)
async def delete_user(user_id: int,  session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    session.delete(db_user)
    session.commit()

    return db_user
