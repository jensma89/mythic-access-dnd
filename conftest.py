"""
conftest.py

Pytest configuration to use test database instead of production database.
This file is automatically loaded by pytest before running tests.
"""
import os
import sys
from pathlib import Path



# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set test database URL BEFORE any imports that might use dependencies.py
os.environ['DATABASE_URL'] = 'sqlite:///./models/db_models/test.db.sql'
