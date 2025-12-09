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

# ALWAYS set SECRET_KEY if not already set (for tests to work)
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only-do-not-use-in-production'
