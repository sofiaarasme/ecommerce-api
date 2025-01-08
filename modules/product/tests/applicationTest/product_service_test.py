import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from modules.product.infrastructure.product_model import Product
from modules.product.domain.product_repository_interface import ProductRepository
from modules.product.application.product_service import ProductService

@pytest.fixture
def mock_repository():
    return MagicMock(spec=ProductRepository)

@pytest.fixture
def product_service(mock_repository):
    return ProductService(repository=mock_repository)

def test_get_all_products(product_service, mock_repository):
    mock_product = Product(id=uuid4(), code='P001', name='Product 1', description='Description 1', price=100, margin=20, cost=80, created_at='2022-01-01', updated_at='2022-01-01', is_active=True)
    mock_repository.get_all.return_value = [mock_product]
    
    products = product_service.get_all_products()
    
    assert len(products) == 1
    assert products[0].code == 'P001'
    mock_repository.get_all.assert_called_once()

def test_get_product_by_id(product_service, mock_repository):
    mock_product = Product(id=uuid4(), code='P001', name='Product 1', description='Description 1', price=100, margin=20, cost=80, created_at='2022-01-01', updated_at='2022-01-01', is_active=True)
    mock_repository.get_by_id.return_value = mock_product
    
    product = product_service.get_product_by_id(mock_product.id)
    
    assert product.code == 'P001'
    mock_repository.get_by_id.assert_called_once_with(mock_product.id)

def test_create_new_product(product_service, mock_repository):
    product_data = {
        "id": uuid4(),
        "code": 'P001',
        "name": 'Product 1',
        "description": 'Description 1',
        "price": 100,
        "margin": 20,
        "cost": 80,
        "created_at": '2022-01-01',
        "updated_at": '2022-01-01',
        "is_active": True
    }
    mock_product = Product(**product_data)
    mock_repository.create.return_value = mock_product

    created_product = product_service.create_new_product(product_data)

    assert created_product.code == 'P001'
    mock_repository.create.assert_called_once()
    called_args = mock_repository.create.call_args[0][0]

    # Comparar las propiedades del objeto en lugar del objeto entero
    assert called_args.id == mock_product.id
    assert called_args.code == mock_product.code
    assert called_args.name == mock_product.name

def test_update_product(product_service, mock_repository):
    mock_product = Product(id=uuid4(), code='P001', name='Product 1', description='Description 1', price=100, margin=20, cost=80, created_at='2022-01-01', updated_at='2022-01-01', is_active=True)
    updated_data = {"name": "Updated Product 1"}
    updated_product = Product(id=mock_product.id, code='P001', name='Updated Product 1', description='Description 1', price=100, margin=20, cost=80, created_at='2022-01-01', updated_at='2022-01-01', is_active=True)
    mock_repository.update.return_value = updated_product
    
    result = product_service.update_product(mock_product.id, updated_data)
    
    assert result.name == 'Updated Product 1'
    mock_repository.update.assert_called_once_with(mock_product.id, updated_data)

def test_delete_product(product_service, mock_repository):
    mock_product_id = uuid4()
    product_service.delete_product(mock_product_id)
    
    mock_repository.delete.assert_called_once_with(mock_product_id)
