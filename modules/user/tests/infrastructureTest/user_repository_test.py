import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Base
from modules.user.infrastructure.user_model import User, Role
from modules.user.infrastructure.user_repository import UserRepositoryImplementation
from modules.carts.infrastructure.car_model import Cart

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def engine():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def user_repository(session):
    return UserRepositoryImplementation(db=session)

def test_register_user(user_repository, session):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "password",
        "role": Role.CUSTOMER.value
    }
    user = User(**user_data)
    registered_user = user_repository.register(user)
    assert registered_user.id is not None
    assert registered_user.email == "test@example.com"
