import pytest
from uuid import uuid4, UUID
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.inventory.infrastructure.inventory_model import InventoryModel
from modules.inventory.infrastructure.inventory_repository import InventoryRepositoryImplementation
from config import Base

@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope="module")
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def session_factory(engine, create_tables):
    return sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def session(session_factory):
    session = session_factory()
    yield session
    session.close()

@pytest.fixture(scope="function")
def repo(session):
    return InventoryRepositoryImplementation(db=session)

def test_get_inventory(session, repo):
    product_id = uuid4()
    inventory = InventoryModel(
        id=uuid4(),
        product_id=product_id,
        quantity=10
    )
    session.add(inventory)
    session.commit()

    result = repo.get_inventory(product_id=product_id)
    assert result is not None
    assert result.product_id == product_id
    assert result.quantity == 10

def test_save_inventory(session, repo):
    inventory = InventoryModel(
        id=uuid4(),
        product_id=uuid4(),
        quantity=15
    )

    repo.save_inventory(inventory=inventory)

    result = session.query(InventoryModel).filter_by(id=inventory.id).first()
    assert result is not None
    assert result.product_id == inventory.product_id
    assert result.quantity == 15

def test_update_inventory(session, repo):
    product_id = uuid4()
    inventory = InventoryModel(
        id=uuid4(),
        product_id=product_id,
        quantity=20
    )
    session.add(inventory)
    session.commit()

    inventory.quantity = 30
    repo.update_inventory(inventory=inventory)

    result = session.query(InventoryModel).filter_by(id=inventory.id).first()
    assert result is not None
    assert result.quantity == 30
