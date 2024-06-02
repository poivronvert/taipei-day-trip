from sqlmodel import create_engine, SQLModel

from config import settings
from models import *
from crud import add_attraction_from_json

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_table()
    add_attraction_from_json("data/taipei-attractions.json")
