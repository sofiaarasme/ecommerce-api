import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from config import Base
from modules.user.infrastructure.user_model import User, Role

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(session):
    new_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        role=Role.CUSTOMER.value
    )
    session.add(new_user)
    session.commit()

    retrieved_user = session.query(User).filter_by(email="test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.hashed_password == "hashed_password"
    assert retrieved_user.role == Role.CUSTOMER.value

def test_update_user(session):
    user = session.query(User).filter_by(email="test@example.com").first()
    user.email = "new_email@example.com"
    session.commit()

    updated_user = session.query(User).filter_by(email="new_email@example.com").first()
    assert updated_user is not None
    assert updated_user.email == "new_email@example.com"

def test_delete_user(session):
    user = session.query(User).filter_by(email="new_email@example.com").first()
    session.delete(user)
    session.commit()

    deleted_user = session.query(User).filter_by(email="new_email@example.com").first()
    assert deleted_user is None
