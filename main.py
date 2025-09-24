"""
main.py

Webserver entry
"""
from fastapi import FastAPI
from dependencies import create_db_and_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the tables and start and stop the DB session"""
    create_db_and_tables() # Create the tables
    print("Server started!")
    yield
    print("Server stopped!")


app = FastAPI(lifespan=lifespan)
