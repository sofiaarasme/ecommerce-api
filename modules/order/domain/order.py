from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from .order_item import OrderItemInterface
from datetime import datetime

class OrderInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def user_id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def created_at(self) -> datetime:
        pass

    @property
    @abstractmethod
    def updated_at(self) -> datetime:
        pass

    @property
    @abstractmethod
    def total_amount(self) -> float:
        pass

    @property
    @abstractmethod
    def status(self) -> str:
        pass

    @property
    @abstractmethod
    def items(self) -> List[OrderItemInterface]:
        pass