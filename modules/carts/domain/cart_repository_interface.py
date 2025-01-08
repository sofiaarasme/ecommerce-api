from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from modules.carts.domain.cart import CartInterface
from modules.carts.domain.cart_item import CartItemInterface

class CartRepositoryInterface(ABC):

    @abstractmethod
    def get_cart(self, user_id: UUID) -> CartInterface:
        pass

    @abstractmethod
    def create_cart(self, cart_data: dict) -> CartInterface:
        pass

    @abstractmethod
    def add_cart_item(self, cart_id: UUID, item_data: dict) -> CartItemInterface:
        pass

    @abstractmethod
    def get_cart_items(self, cart_id: UUID) -> List[CartItemInterface]:
        pass

    @abstractmethod
    def update_cart_item(self, item_id: UUID, quantity: int) -> CartItemInterface:
        pass

    @abstractmethod
    def delete_cart_item(self, item_id: UUID) -> None:
        pass
