from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url

from .settings import settings


def _connect_args_from_url(database_url: str) -> dict:
    url = make_url(database_url)
    # SQLite needs this flag for multi-threaded FastAPI usage; other engines don't.
    if url.get_backend_name() == "sqlite":
        return {"check_same_thread": False}
    return {}


DATABASE_URL = settings.database_url
engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args_from_url(DATABASE_URL),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
