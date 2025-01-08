import pytest
from pydantic import BaseModel, ValidationError, conint
from typing import List
from uuid import uuid4, UUID
from modules.carts.application.dtos.create_cart_dto import CartItemDto, CartCreateDto

# Pruebas unitarias
def test_cart_item_dto_valid():
    data = {
        "cart_id": uuid4(),
        "product_id": uuid4(),
        "quantity": 2
    }
    cart_item = CartItemDto(**data)
    assert cart_item.cart_id == data["cart_id"]
    assert cart_item.product_id == data["product_id"]
    assert cart_item.quantity == data["quantity"]

def test_cart_item_dto_invalid_quantity():
    data = {
        "cart_id": uuid4(),
        "product_id": uuid4(),
        "quantity": -1  # Invalid quantity
    }
    try:
        CartItemDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('quantity',)
        assert e.errors()[0]['msg'] == 'ensure this value is greater than or equal to 0'

def test_cart_create_dto_valid():
    item_data = {
        "cart_id": uuid4(),
        "product_id": uuid4(),
        "quantity": 2
    }
    cart_data = {
        "items": [item_data]
    }
    cart = CartCreateDto(**cart_data)
    assert len(cart.items) == 1
    assert cart.items[0].cart_id == item_data["cart_id"]
    assert cart.items[0].product_id == item_data["product_id"]
    assert cart.items[0].quantity == item_data["quantity"]

def test_cart_create_dto_invalid_item():
    item_data = {
        "cart_id": uuid4(),
        "product_id": uuid4(),
        "quantity": -1  # Invalid quantity
    }
    cart_data = {
        "items": [item_data]
    }
    try:
        CartCreateDto(**cart_data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('items', 0, 'quantity')
        assert e.errors()[0]['msg'] == 'ensure this value is greater than or equal to 0'

def test_cart_create_dto_empty_items():
    cart_data = {
        "items": []  # Empty items list
    }
    cart = CartCreateDto(**cart_data)
    assert len(cart.items) == 0
