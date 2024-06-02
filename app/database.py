from sqlmodel import create_engine

from config import settings


_DATABASE_URL = settings.database_url

engine = create_engine(_DATABASE_URL, echo=True)