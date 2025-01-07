from abc import ABC, abstractmethod

class ProductInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> int:
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
    def price(self) -> int:
        pass

    @property
    @abstractmethod
    def is_active(self) -> bool:
        pass