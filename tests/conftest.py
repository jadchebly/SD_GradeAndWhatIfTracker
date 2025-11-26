# tests/conftest.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

# Import your app + SQLAlchemy Base + get_db dependency
from backend.app import app
from backend.models import Base
from backend.app import get_db  # if get_db lives in app.py, change to: from backend.app import get_db

# --- Single shared in-memory SQLite across all connections/threads ---
engine = create_engine(
    "sqlite://",                     # note: no '///' – this uses a memory DB shared by StaticPool
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a fresh schema before each test (so tests don't bleed into each other)
@pytest.fixture(autouse=True)
def _create_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

# Override the app's get_db dependency so routes use our test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Provide a test client
@pytest.fixture
def client():
    return TestClient(app)
