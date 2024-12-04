from sqlmodel import create_engine, Session, SQLModel, text
from config import settings


DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

with Session(engine) as session:
    statement=text("CREATE DATABASE IF NOT EXISTS taipeitrip")
    session.exec(statement)

def create_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()