import pytest
from pydantic import ValidationError
from modules.product.application.dtos.product_update_dto import ProductUpdateDto

def test_valid_product_update_dto():
    dto = ProductUpdateDto(
        code='P001',
        name='Updated Product 1',
        price=150.0,
        cost=120.0,
        margin=30.0,
        description='Updated description of Product 1'
    )
    assert dto.code == 'P001'
    assert dto.name == 'Updated Product 1'
    assert dto.price == 150.0
    assert dto.cost == 120.0
    assert dto.margin == 30.0
    assert dto.description == 'Updated description of Product 1'

def test_partial_update_product_update_dto():
    dto = ProductUpdateDto(
        price=150.0
    )
    assert dto.price == 150.0
    assert dto.code is None
    assert dto.name is None
    assert dto.cost is None
    assert dto.margin is None
    assert dto.description is None

def test_invalid_price_type():
    with pytest.raises(ValidationError):
        ProductUpdateDto(
            price='not a float'  # Valor inválido
        )

def test_invalid_margin_type():
    with pytest.raises(ValidationError):
        ProductUpdateDto(
            margin='not a float'  # Valor inválido
        )

def test_invalid_cost_type():
    with pytest.raises(ValidationError):
        ProductUpdateDto(
            cost='not a float'  # Valor inválido
        )
