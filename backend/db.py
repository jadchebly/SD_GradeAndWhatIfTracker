from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
import os

from .settings import settings


def _connect_args_from_url(database_url: str) -> dict:
    url = make_url(database_url)
    # SQLite needs this flag for multi-threaded FastAPI usage; other engines don't.
    if url.get_backend_name() == "sqlite":
        return {"check_same_thread": False}
    return {}


DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "postgresql://",
    "postgresql+psycopg2binary://"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
