from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
from modules.carts.infrastructure.car_model import Cart
from modules.carts.infrastructure.car_model import CartItem
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface

class CartRepositoryImplementation(CartRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_cart(self, user_id: UUID) -> Cart:
        return self.db.query(Cart).filter(Cart.user_id == user_id).first()

    def create_cart(self, cart: Cart) -> Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def add_cart_item(self, item: CartItem) -> CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_cart_items(self, cart_id: UUID) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    def update_cart_item(self, product_id: UUID, quantity: int) -> CartItem:
        db_item = self.db.query(CartItem).filter(CartItem.product_id == product_id).first()
        if db_item:
            db_item.quantity = quantity
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete_cart_item(self, product_id: UUID) -> None:
        db_item = self.db.query(CartItem).filter(CartItem.product_id == product_id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
