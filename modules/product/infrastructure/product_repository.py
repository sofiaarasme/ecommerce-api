from sqlalchemy.orm import Session
from typing import List
from modules.product.infrastructure.product_model import Product
from modules.product.domain.product_repository_interface import ProductRepository

class ProductRepositoryImplementation(ProductRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product_id: int, product_data: dict) -> Product:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        for key, value in product_data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        self.db.delete(product)
        self.db.commit()