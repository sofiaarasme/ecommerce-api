import pytest
from pydantic import ValidationError
from modules.product.application.dtos.product_create_dto import ProductCreateDto

def test_valid_product_create_dto():
    data = {
        "code": "SP123",
        "name": "Sample Product",
        "description": "This is a sample product",
        "margin": 0.25,
        "cost": 10.0,
        "is_active": True
    }
    product = ProductCreateDto(**data)
    assert product.code == data["code"]
    assert product.name == data["name"]
    assert product.description == data["description"]
    assert product.margin == data["margin"]
    assert product.cost == data["cost"]
    assert product.is_active == data["is_active"]
    assert product.price == pytest.approx(13.33, rel=1e-2)  # Verificando el precio calculado (10 / (1 - 0.25))

def test_default_is_active():
    data = {
        "code": "SP123",
        "name": "Sample Product",
        "description": "This is a sample product",
        "margin": 0.25,
        "cost": 10.0
    }
    product = ProductCreateDto(**data)
    assert product.is_active is True
    assert product.price == pytest.approx(13.33, rel=1e-2)  # Verificando el precio calculado (10 / (1 - 0.25))

def test_invalid_product_margin():
    data = {
        "code": "SP123",
        "name": "Sample Product",
        "description": "This is a sample product",
        "margin": 1.5,  # Invalid margin
        "cost": 10.0,
        "is_active": True
    }
    with pytest.raises(ValidationError):
        ProductCreateDto(**data)

