import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from passlib.context import CryptContext

from app.database.session import Base
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.role import Role
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def create_test_user(db, username: str, email: str, role: Role):
    """
    Create a test user with the specified role.
    """
    user = User(
        username=username,
        email=email,
        role=role,
        hashed_password=hash_password("TestPass123"),
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_superuser(db):
    return create_test_user(db, "superuser", "superuser@example.com", Role.SUPERUSER)

@pytest.fixture
def test_editor(db):
    return create_test_user(db, "editor", "editor@example.com", Role.EDITOR)

@pytest.fixture
def test_viewer(db):
    return create_test_user(db, "viewer", "viewer@example.com", Role.VIEWER)

def create_client_with_user(client, user):
    """
    Overrides the get_current_user dependency for testing with a specific user.
    """
    def override_get_current_user():
        return user
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_superuser(client, test_superuser):
    return create_client_with_user(client, test_superuser)

@pytest.fixture
def client_with_editor(client, test_editor):
    return create_client_with_user(client, test_editor)

@pytest.fixture
def client_with_viewer(client, test_viewer):
    return create_client_with_user(client, test_viewer)