import pytest
from pydantic import BaseModel, ValidationError
from uuid import UUID, uuid4

# Definición del modelo
class CartItemUpdateDto(BaseModel):
    product_id: UUID
    quantity: int

# Pruebas unitarias
def test_cart_item_update_dto_valid():
    data = {
        "product_id": uuid4(),
        "quantity": 3
    }
    cart_item_update = CartItemUpdateDto(**data)
    assert cart_item_update.product_id == data["product_id"]
    assert cart_item_update.quantity == data["quantity"]

def test_cart_item_update_dto_invalid_quantity():
    data = {
        "product_id": uuid4(),
        "quantity": -1 
    }
    try:
        CartItemUpdateDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('quantity',)
        assert e.errors()[0]['msg'] == 'ensure this value is greater than or equal to 0'

def test_cart_item_update_dto_missing_product_id():
    data = {
        "quantity": 3
    }
    try:
        CartItemUpdateDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('product_id',)
        assert e.errors()[0]['msg'] == 'Field required'

def test_cart_item_update_dto_missing_quantity():
    data = {
        "product_id": uuid4()
    }
    try:
        CartItemUpdateDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('quantity',)
        assert e.errors()[0]['msg'] == 'Field required'
