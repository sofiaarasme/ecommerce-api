import pytest
from unittest.mock import MagicMock
from uuid import uuid4, UUID
from modules.order.domain.order_repository_interface import OrderRepository
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface
from modules.user.infrastructure.user_model import User, Role
from modules.order.infrastructure.order_model import Order, OrderItem, OrderStatus
from modules.order.application.order_service import OrderService

@pytest.fixture
def mock_order_repository():
    return MagicMock(OrderRepository)

@pytest.fixture
def mock_cart_repository():
    return MagicMock(CartRepositoryInterface)

@pytest.fixture
def order_service(mock_order_repository, mock_cart_repository):
    return OrderService(order_repository=mock_order_repository, cart_repository=mock_cart_repository)

def test_create_order_from_cart(order_service, mock_cart_repository, mock_order_repository):
    user_id = uuid4()
    current_user = User(id=user_id, username="testuser", email="test@example.com")

    product_id = uuid4()
    mock_cart_item = MagicMock()
    mock_cart_item.product_id = product_id
    mock_cart_item.quantity = 2
    mock_cart_item.product.price = 10.0

    mock_cart = MagicMock()
    mock_cart.items = [mock_cart_item]
    mock_cart_repository.get_cart.return_value = mock_cart

    order_service.create_order_from_cart(current_user)

    mock_order_repository.create_order.assert_called_once()
    mock_order_repository.add_order_item.assert_called_once()
    created_order = mock_order_repository.create_order.call_args[0][0]
    created_order_item = mock_order_repository.add_order_item.call_args[0][0]

    assert created_order.user_id == user_id
    assert created_order.total_amount == 20.0
    assert created_order.status == 'pending'
    assert created_order_item.order_id == created_order.id
    assert created_order_item.product_id == product_id
    assert created_order_item.quantity == 2

def test_get_user_orders(order_service, mock_order_repository):
    user_id = uuid4()
    mock_orders = [MagicMock(Order), MagicMock(Order)]
    mock_order_repository.get_user_orders.return_value = mock_orders

    user_orders = order_service.get_user_orders(user_id)
    mock_order_repository.get_user_orders.assert_called_once_with(user_id)
    assert user_orders == mock_orders

def test_get_order_by_id(order_service, mock_order_repository):
    order_id = uuid4()
    mock_order = MagicMock(Order)
    mock_order_repository.get_order_by_id.return_value = mock_order

    order = order_service.get_order_by_id(order_id)
    mock_order_repository.get_order_by_id.assert_called_once_with(order_id)
    assert order == mock_order


