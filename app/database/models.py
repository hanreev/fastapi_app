from app.models.user import UserInDB
from sqlmodel import SQLModel

from .core import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
