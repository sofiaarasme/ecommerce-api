from abc import ABC, abstractmethod
from uuid import UUID

class ProductInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def code(self) -> str:
        pass
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @property
    @abstractmethod
    def cost(self) -> float:
        pass

    @property
    @abstractmethod
    def margin(self) -> float:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass
    
    @property
    @abstractmethod
    def created_at(self) -> str:
        pass

    @property
    @abstractmethod
    def updated_at(self) -> str:
        pass

    @property
    @abstractmethod
    def is_active(self) -> bool:
        pass