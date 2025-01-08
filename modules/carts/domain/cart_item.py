from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

class CartItemInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def cart_id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def product_id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
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
    def cart(self):
        pass

    @property
    @abstractmethod
    def product(self):
        pass
