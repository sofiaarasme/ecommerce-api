from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from datetime import datetime

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

class ProductImplementation(ProductInterface):
    def __init__(self, id: UUID, code: str, name: str, description: str, cost: float, margin: float, price: float, created_at: str, updated_at: str, is_active: bool):
        self._id = id
        self._code = code
        self._name = name
        self._description = description
        self._cost = cost
        self._margin = margin
        self._price = price
        self._created_at = created_at
        self._updated_at = updated_at
        self._is_active = is_active

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def code(self) -> str:
        return self._code
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def cost(self) -> float:
        return self._cost

    @property
    def margin(self) -> float:
        return self._margin

    @property
    def price(self) -> float:
        return self._price
    
    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

    @property
    def is_active(self) -> bool:
        return self._is_active
