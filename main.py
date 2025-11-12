"""
main.py

Webserver entry and links to routes.
"""
from fastapi import FastAPI
from dependencies import create_db_and_tables
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from rate_limit import limiter
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, campaigns, classes, dices, dicesets, dicelogs, users
import logging



logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the tables and start and stop the DB session"""
    create_db_and_tables() # Create the tables
    logger.info("Server started and DB tables ensured")
    yield
    logger.info("Server stopped!")

app = FastAPI(lifespan=lifespan)

# Attach limiter to app state
app.state.limiter = limiter

# Register middleware
app.add_middleware(SlowAPIMiddleware)

# Register error handler (helper from slowapi)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS middleware
origins = [
    "https://www.mythic-access-dnd.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Link to routes
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(classes.router)
app.include_router(dices.router)
app.include_router(dicesets.router)
app.include_router(dicelogs.router)
app.include_router(auth_routes.router)


@app.get("/healthz")
def health_check():
    """A health check for deploying (on commit)."""
    return {"status": "ok"}
