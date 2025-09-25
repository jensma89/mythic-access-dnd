"""
main.py

Webserver entry
"""
from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Query
from dependencies import create_db_and_tables, SessionDep
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from models.db_models.table_models import Campaign, User
from models.schemas.user_schema import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the tables and start and stop the DB session"""
    create_db_and_tables() # Create the tables
    print("Server started!")
    yield
    print("Server stopped!")


app = FastAPI(lifespan=lifespan)



@app.get("/users/", response_model=List[UserPublic])
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


@app.post("/users/", response_model=UserPublic)
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



@app.put("/users/{user_id}", response_model=UserPublic)
async def update_user(user: UserUpdate, session: SessionDep):
    pass


@app.delete("/users/{user_id}", response_model=UserPublic)
async def delete_user(session: SessionDep):
    pass