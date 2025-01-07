from abc import ABC, abstractmethod
from typing import List
from .product import ProductInterface

class ProductRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[ProductInterface]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> ProductInterface:
        pass

    @abstractmethod
    def create(self, product: ProductInterface) -> ProductInterface:
        pass

    @abstractmethod
    def update(self, product_id: int, product_data: dict) -> ProductInterface:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass