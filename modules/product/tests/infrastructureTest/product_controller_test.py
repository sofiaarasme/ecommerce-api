""" import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Base, get_db
from main import app  # Asegúrate de ajustar la ruta según tu estructura de proyecto
from modules.product.infrastructure.product_model import Product
from modules.product.application.dtos.product_create_dto import ProductCreateDto
from modules.product.application.dtos.product_update_dto import ProductUpdateDto
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
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# Pruebas unitarias para la API de productos
def test_read_products(client, session):
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

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [{
        "id": str(product.id),
        "code": "P001",
        "name": "Product 1",
        "description": "Description 1",
        "cost": 100.0,
        "margin": 20.0,
        "price": 120.0,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
        "is_active": True
    }]

def test_read_product(client, session):
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

    response = client.get(f"/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": str(product.id),
        "code": "P002",
        "name": "Product 2",
        "description": "Description 2",
        "cost": 200.0,
        "margin": 25.0,
        "price": 250.0,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
        "is_active": True
    }

def test_create_product(client):
    product_data = {
        "code": "P003",
        "name": "Product 3",
        "description": "Description 3",
        "cost": 300.0,
        "margin": 30.0,
        "price": 330.0,
        "is_active": True
    }
    response = client.post("/", json=product_data)
    assert response.status_code == 200
    created_product = response.json()
    assert created_product["code"] == "P003"
    assert created_product["name"] == "Product 3"

def test_update_product(client, session):
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
    
    updated_data = {"name": "Updated Product 4"}
    response = client.put(f"/{product_id}", json=updated_data)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == "Updated Product 4"

def test_delete_product(client, session):
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
    
    response = client.delete(f"/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
    deleted_product = session.query(Product).filter_by(id=product_id).first()
    assert deleted_product is None
 """