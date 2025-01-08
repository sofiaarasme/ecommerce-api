import pytest
from uuid import uuid4, UUID
from datetime import datetime
from product_interface import ProductImplementation 

@pytest.fixture
def product():
    return ProductImplementation(
        id=uuid4(),
        code='P001',
        name='Product 1',
        description='Description of Product 1',
        cost=100.0,
        margin=20.0,
        price=120.0,
        created_at=str(datetime.utcnow()),
        updated_at=str(datetime.utcnow()),
        is_active=True
    )

def test_product_id(product):
    assert isinstance(product.id, UUID)

def test_product_code(product):
    assert product.code == 'P001'

def test_product_name(product):
    assert product.name == 'Product 1'

def test_product_description(product):
    assert product.description == 'Description of Product 1'

def test_product_cost(product):
    assert product.cost == 100.0

def test_product_margin(product):
    assert product.margin == 20.0

def test_product_price(product):
    assert product.price == 120.0

def test_product_created_at(product):
    assert isinstance(product.created_at, str)

def test_product_updated_at(product):
    assert isinstance(product.updated_at, str)

def test_product_is_active(product):
    assert product.is_active is True
