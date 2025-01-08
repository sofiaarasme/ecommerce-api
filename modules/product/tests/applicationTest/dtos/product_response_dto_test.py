import pytest
from pydantic import ValidationError
from modules.product.application.dtos.product_response_dto import ProductResponseDto  # Asegúrate de ajustar la ruta según tu estructura de proyecto

def test_valid_product_response_dto():
    dto = ProductResponseDto(
        id=1,
        name='Product 1',
        description='Description of Product 1',
        price=120,
        is_active=True
    )
    assert dto.id == 1
    assert dto.name == 'Product 1'
    assert dto.description == 'Description of Product 1'
    assert dto.price == 120
    assert dto.is_active is True

def test_invalid_price_type():
    with pytest.raises(ValidationError):
        ProductResponseDto(
            id=1,
            name='Product 1',
            description='Description of Product 1',
            price='not an int',  # Valor inválido
            is_active=True
        )

def test_missing_name():
    with pytest.raises(ValidationError):
        ProductResponseDto(
            id=1,
            description='Description of Product 1',
            price=120,
            is_active=True
        )

def test_default_is_active():
    dto = ProductResponseDto(
        id=1,
        name='Product 1',
        description='Description of Product 1',
        price=120,
        is_active=True
    )
    assert dto.is_active is True
