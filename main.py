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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the tables and start and stop the DB session"""
    create_db_and_tables() # Create the tables
    print("Server started!")
    yield
    print("Server stopped!")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello world"}


@app.get("/users/", response_model=List[User])
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


