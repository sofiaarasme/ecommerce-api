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
        db_cart = self.db.query(Cart).filter(Cart.user_id == user_id).first()
        if db_cart:
            return Cart(
                id=db_cart.id,
                user_id=db_cart.user_id,
                created_at=db_cart.created_at,
                updated_at=db_cart.updated_at,
                user=db_cart.user,
                items=db_cart.items
            )
        return None

    def create_cart(self, cart_data: Cart) -> Cart:
        db_cart = Cart(
            user_id=cart_data.user_id,
            created_at=cart_data.created_at,
            updated_at=cart_data.updated_at
        )
        self.db.add(db_cart)
        self.db.commit()
        self.db.refresh(db_cart)
        return db_cart

    def add_cart_item(self, cart_id: UUID, item_data: CartItem) -> CartItem:
        db_item = CartItem(
            cart_id=cart_id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            created_at=item_data.created_at,
            updated_at=item_data.updated_at
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_cart_items(self, cart_id: UUID) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    def update_cart_item(self, item_id: UUID, quantity: int) -> CartItem:
        db_item = self.db.query(CartItem).filter(CartItem.id == item_id).first()
        if db_item:
            db_item.quantity = quantity
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete_cart_item(self, item_id: UUID) -> None:
        db_item = self.db.query(CartItem).filter(CartItem.id == item_id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
