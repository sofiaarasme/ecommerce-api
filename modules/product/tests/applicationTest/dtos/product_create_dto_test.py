import pytest
from pydantic import ValidationError
from modules.product.application.dtos.product_create_dto import ProductCreateDto  # Asegúrate de ajustar la ruta según tu estructura de proyecto

def test_valid_product_create_dto():
    dto = ProductCreateDto(
        code='P001',
        name='Product 1',
        description='Description of Product 1',
        price=120.0,
        margin=20.0,
        cost=100.0,
        is_active=True
    )
    assert dto.code == 'P001'
    assert dto.name == 'Product 1'
    assert dto.description == 'Description of Product 1'
    assert dto.price == 120.0
    assert dto.margin == 20.0
    assert dto.cost == 100.0
    assert dto.is_active is True

def test_invalid_price_type():
    with pytest.raises(ValidationError):
        ProductCreateDto(
            code='P001',
            name='Product 1',
            description='Description of Product 1',
            price='not a float',  # Valor inválido
            margin=20.0,
            cost=100.0,
            is_active=True
        )

def test_missing_code():
    with pytest.raises(ValidationError):
        ProductCreateDto(
            name='Product 1',
            description='Description of Product 1',
            price=120.0,
            margin=20.0,
            cost=100.0,
            is_active=True
        )

def test_default_is_active():
    dto = ProductCreateDto(
        code='P001',
        name='Product 1',
        description='Description of Product 1',
        price=120.0,
        margin=20.0,
        cost=100.0
    )
    assert dto.is_active is True
