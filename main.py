"""
main.py

Webserver entry
"""
from fastapi import FastAPI
from dependencies import create_db_and_tables
from contextlib import asynccontextmanager
from routes import campaigns,classes, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the tables and start and stop the DB session"""
    create_db_and_tables() # Create the tables
    print("Server started!")
    yield
    print("Server stopped!")


app = FastAPI(lifespan=lifespan)

# Link to routes
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(classes.router)
