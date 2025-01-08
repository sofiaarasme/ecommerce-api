from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

class CartInterface(ABC):

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
    def user(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass
