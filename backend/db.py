import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url


def _connect_args_from_url(db_url: str) -> dict:
    """Detect correct connect_args based on backend."""
    url = make_url(db_url)

    # SQLite requires this for FastAPI multithreading
    if url.get_backend_name() == "sqlite":
        return {"check_same_thread": False}

    # Postgres / MySQL / others do not need connect_args
    return {}


# Load DATABASE_URL safely
raw_url = os.getenv("DATABASE_URL")

if raw_url:
    # Railway provides postgresql:// which needs to be adapted
    DATABASE_URL = raw_url.replace(
        "postgresql://",
        "postgresql+psycopg2binary://"
    )
else:
    # Fallback: used in GitHub Actions tests
    DATABASE_URL = "sqlite:///./test.db"


# Create engine with proper connect args
engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args_from_url(DATABASE_URL)
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
