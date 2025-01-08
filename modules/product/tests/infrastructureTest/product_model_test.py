import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.product.infrastructure.product_model import Product
from config import Base
from uuid import uuid4
from datetime import datetime

# Configuración de fixtures de pytest
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

# Pruebas unitarias para el modelo Product
def test_create_product(session):
    product = Product(
        id=uuid4(),
        code='P001',
        name='Product 1',
        description='Description 1',
        cost=100.0,
        margin=20.0,
        price=120.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )
    session.add(product)
    session.commit()

    result = session.query(Product).filter_by(code='P001').one()
    assert result is not None
    assert result.name == 'Product 1'
    assert result.description == 'Description 1'
    assert result.cost == 100.0
    assert result.margin == 20.0
    assert result.price == 120.0
    assert result.is_active is True

def test_update_product(session):
    product = session.query(Product).filter_by(code='P001').one()
    product.name = 'Updated Product 1'
    session.commit()

    updated_product = session.query(Product).filter_by(code='P001').one()
    assert updated_product.name == 'Updated Product 1'

def test_delete_product(session):
    product = session.query(Product).filter_by(code='P001').one()
    session.delete(product)
    session.commit()

    result = session.query(Product).filter_by(code='P001').first()
    assert result is None
