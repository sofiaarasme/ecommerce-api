from typing import List
from uuid import UUID
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface
from modules.carts.infrastructure.car_model import Cart, CartItem

class CartService:

    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def get_cart(self, user_id: UUID) -> Cart:
        return self.repository.get_cart(user_id)

    def create_cart(self, cart_data: dict) -> Cart:
        new_cart = Cart(**cart_data)
        return self.repository.create_cart(new_cart)

    def add_cart_item(self, cart_id: UUID, item_data: dict) -> CartItem:
        new_cart_item = CartItem(**item_data)
        return self.repository.add_cart_item(cart_id, new_cart_item)

    def get_cart_items(self, cart_id: UUID) -> List[CartItem]:
        return self.repository.get_cart_items(cart_id)

    def update_cart_item(self, item_id: UUID, quantity: int) -> CartItem:
        return self.repository.update_cart_item(item_id, quantity)

    def delete_cart_item(self, item_id: UUID) -> None:
        return self.repository.delete_cart_item(item_id)
