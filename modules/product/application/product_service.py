from typing import List
from modules.product.infrastructure.product_model import Product
from modules.product.domain.product_repository_interface import ProductRepository

class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.repository.get_by_id(product_id)

    def create_new_product(self, product_data: dict):
        new_product = Product(**product_data)
        return self.repository.create(new_product)

    def update_product(self, product_id: int, product_data: dict):
        return self.repository.update(product_id, product_data)

    def delete_product(self, product_id: int):
        return self.repository.delete(product_id)