import pytest
from uuid import uuid4
from pydantic import BaseModel, ValidationError
from modules.order.infrastructure.order_model import OrderStatus
from modules.order.application.dtos.update_order_dto import UpdateOrderDto

def test_update_order_dto_valid():
    data = {
        "order_id": uuid4(),
        "status": OrderStatus.PENDING
    }
    update_order = UpdateOrderDto(**data)
    assert update_order.order_id == data["order_id"]
    assert update_order.status == data["status"]

def test_update_order_dto_invalid_status():
    data = {
        "order_id": uuid4(),
        "status": "invalid_status"  # Invalid status
    }
    try:
        UpdateOrderDto(**data)
    except ValidationError as e:
        assert e.errors()[0]['loc'] == ('status',)
        assert 'value is not a valid enumeration member' in e.errors()[0]['msg']

def test_update_order_dto_missing_order_id():
    data = {
        "status": OrderStatus.PENDING
    }
    with pytest.raises(ValidationError):
        UpdateOrderDto(**data)

def test_update_order_dto_missing_status():
    data = {
        "order_id": uuid4()
    }
    with pytest.raises(ValidationError):
        UpdateOrderDto(**data)
