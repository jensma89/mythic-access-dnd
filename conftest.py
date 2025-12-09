"""
conftest.py

Pytest configuration - sets environment variables before any imports.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables BEFORE any imports
os.environ['DATABASE_URL'] = 'sqlite:///./models/db_models/test.db.sql'

# For SECRET_KEY: Use environment variable if set (in CI), otherwise use test key
if 'SECRET_KEY' not in os.environ:
    os.environ['SECRET_KEY'] = 'test-secret-key-for-local-testing-only'
