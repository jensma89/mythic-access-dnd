"""
models.py

Table models for DB.
"""
from sqlmodel import Field, SQLModel, select



class User(SQLModel, table=True):

