from abc import ABC, abstractmethod
from uuid import UUID

class InventoryInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass

    @property
    @abstractmethod
    def product_id(self) -> UUID:
        pass
    
    @property
    @abstractmethod
    def created_at(self) -> str:
        pass

    @property
    @abstractmethod
    def updated_at(self) -> str:
        pass