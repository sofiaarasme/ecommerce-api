import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.product.infrastructure.product_model import Product
from modules.product.infrastructure.product_repository import ProductRepositoryImplementation
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

@pytest.fixture(scope="function")
def repository(session):
    return ProductRepositoryImplementation(db=session)

# Pruebas unitarias para ProductRepositoryImplementation
def test_get_all_products(repository, session):
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
    
    products = repository.get_all()
    
    assert len(products) == 1
    assert products[0].code == 'P001'

def test_get_product_by_id(repository, session):
    product_id = uuid4()
    product = Product(
        id=product_id,
        code='P002',
        name='Product 2',
        description='Description 2',
        cost=200.0,
        margin=25.0,
        price=250.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )
    session.add(product)
    session.commit()

    fetched_product = repository.get_by_id(product_id)
    
    assert fetched_product is not None
    assert fetched_product.code == 'P002'

def test_create_product(repository, session):
    product_data = {
        'id': uuid4(),
        'code': 'P003',
        'name': 'Product 3',
        'description': 'Description 3',
        'cost': 300.0,
        'margin': 30.0,
        'price': 330.0,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'is_active': True
    }
    product = Product(**product_data)
    
    created_product = repository.create(product)
    
    assert created_product.code == 'P003'
    assert session.query(Product).filter_by(code='P003').one()

def test_update_product(repository, session):
    product_id = uuid4()
    product = Product(
        id=product_id,
        code='P004',
        name='Product 4',
        description='Description 4',
        cost=400.0,
        margin=35.0,
        price=435.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )
    session.add(product)
    session.commit()
    
    updated_data = {'name': 'Updated Product 4'}
    updated_product = repository.update(product_id, updated_data)
    
    assert updated_product.name == 'Updated Product 4'

def test_delete_product(repository, session):
    product_id = uuid4()
    product = Product(
        id=product_id,
        code='P005',
        name='Product 5',
        description='Description 5',
        cost=500.0,
        margin=40.0,
        price=540.0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        is_active=True
    )
    session.add(product)
    session.commit()
    
    repository.delete(product_id)
    
    deleted_product = session.query(Product).filter_by(id=product_id).first()
    assert deleted_product is None
