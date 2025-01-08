import pytest
from unittest.mock import MagicMock, call
from uuid import uuid4, UUID
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface
from modules.carts.infrastructure.car_model import Cart, CartItem
from modules.user.infrastructure.user_model import User
from modules.carts.application.cart_service import CartService

@pytest.fixture
def mock_repository():
    return MagicMock(CartRepositoryInterface)

@pytest.fixture
def cart_service(mock_repository):
    return CartService(repository=mock_repository)

def test_get_cart(cart_service, mock_repository):
    user_id = uuid4()
    mock_cart = Cart(id=uuid4(), user_id=user_id)
    mock_repository.get_cart.return_value = mock_cart

    cart = cart_service.get_cart(user_id)
    mock_repository.get_cart.assert_called_once_with(user_id)
    assert cart == mock_cart

def test_create_cart(cart_service, mock_repository):
    user_id = uuid4()
    current_user = User(id=user_id, username="testuser", email="test@example.com")
    cart_data = {"id": uuid4()}
    mock_cart = Cart(id=cart_data["id"], user_id=user_id)
    mock_repository.create_cart.return_value = mock_cart

    new_cart = cart_service.create_cart(cart_data, current_user)
    mock_repository.create_cart.assert_called_once()
    assert new_cart.id == cart_data["id"]
    assert new_cart.user_id == current_user.id

def test_add_cart_item(cart_service, mock_repository):
    cart_id = uuid4()
    item_data = {"product_id": uuid4(), "quantity": 1}
    mock_cart_item = CartItem(cart_id=cart_id, **item_data)
    mock_repository.add_cart_item.return_value = mock_cart_item

    new_cart_item = cart_service.add_cart_item(cart_id, item_data)
    mock_repository.add_cart_item.assert_called_once()
    assert new_cart_item.cart_id == cart_id
    assert new_cart_item.product_id == item_data["product_id"]
    assert new_cart_item.quantity == item_data["quantity"]

def test_get_cart_items(cart_service, mock_repository):
    cart_id = uuid4()
    mock_cart_items = [
        CartItem(cart_id=cart_id, product_id=uuid4(), quantity=1),
        CartItem(cart_id=cart_id, product_id=uuid4(), quantity=2)
    ]
    mock_repository.get_cart_items.return_value = mock_cart_items

    cart_items = cart_service.get_cart_items(cart_id)
    mock_repository.get_cart_items.assert_called_once_with(cart_id)
    assert cart_items == mock_cart_items

def test_update_cart_item(cart_service, mock_repository):
    product_id = uuid4()
    quantity = 3
    mock_cart_item = CartItem(product_id=product_id, quantity=quantity)
    mock_repository.update_cart_item.return_value = mock_cart_item

    updated_cart_item = cart_service.update_cart_item(product_id, quantity)
    mock_repository.update_cart_item.assert_called_once_with(product_id, quantity)
    assert updated_cart_item.product_id == product_id
    assert updated_cart_item.quantity == quantity

def test_delete_cart_item(cart_service, mock_repository):
    product_id = uuid4()

    cart_service.delete_cart_item(product_id)
    mock_repository.delete_cart_item.assert_called_once_with(product_id)
