import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.inventory.infrastructure.inventory_model import InventoryModel
from modules.product.infrastructure.product_model import Product
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

class TestInventoryModel:

    def test_create_inventory(self, session):
        product = Product(id=uuid4(), code='P001', name="Product 1")
        session.add(product)
        session.commit()

        inventory = InventoryModel(
            product_id=product.id,
            quantity=10
        )
        session.add(inventory)
        session.commit()

        result = session.query(InventoryModel).filter_by(product_id=product.id).one()
        assert result.quantity == 10
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_update_inventory_quantity(self, session):
        product = Product(id=uuid4(), code='P002', name="Product 1")
        session.add(product)
        session.commit()

        inventory = InventoryModel(
            product_id=product.id,
            quantity=10
        )
        session.add(inventory)
        session.commit()

        inventory.quantity = 20
        session.commit()

        result = session.query(InventoryModel).filter_by(product_id=product.id).one()
        assert result.quantity == 20
        assert result.updated_at is not None
