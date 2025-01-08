from abc import ABC, abstractmethod
from .order import OrderInterface, OrderItemInterface
from uuid import UUID
from typing import List

class OrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: OrderInterface) -> OrderInterface:
        pass

    @abstractmethod
    def add_order_item(self, item: OrderItemInterface) -> OrderItemInterface:
        pass

    @abstractmethod
    def get_user_orders(self, user_id: UUID) -> List[OrderInterface]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: UUID) -> OrderInterface:
        pass