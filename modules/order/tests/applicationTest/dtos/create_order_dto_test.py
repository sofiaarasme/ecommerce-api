import pytest
from pydantic import BaseModel, ValidationError
from typing import List
from uuid import UUID, uuid4

class OrderItemDto(BaseModel):
    product_id: UUID
    quantity: int

class OrderCreateDto(BaseModel):
    items: List[OrderItemDto]

def test_order_item_dto_valid():
    data = {
        "product_id": uuid4(),
        "quantity": 2
    }
    order_item = OrderItemDto(**data)
    assert order_item.product_id == data["product_id"]
    assert order_item.quantity == data["quantity"]

def test_order_item_dto_invalid_quantity():
    data = {
        "product_id": uuid4(),
        "quantity": -1  # Invalid quantity
    }
    try:
        OrderItemDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('quantity',)
        assert 'greater than or equal to 0' in e.errors()[0]['msg']

def test_order_create_dto_valid():
    item_data = {
        "product_id": uuid4(),
        "quantity": 2
    }
    order_data = {
        "items": [item_data]
    }
    order = OrderCreateDto(**order_data)
    assert len(order.items) == 1
    assert order.items[0].product_id == item_data["product_id"]
    assert order.items[0].quantity == item_data["quantity"]

def test_order_create_dto_invalid_item():
    item_data = {
        "product_id": uuid4(),
        "quantity": -1  # Invalid quantity
    }
    order_data = {
        "items": [item_data]
    }
    try:
        OrderCreateDto(**order_data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('items', 0, 'quantity')
        assert 'greater than or equal to 0' in e.errors()[0]['msg']

def test_order_create_dto_empty_items():
    order_data = {
        "items": []  # Empty items list
    }
    order = OrderCreateDto(**order_data)
    assert len(order.items) == 0
