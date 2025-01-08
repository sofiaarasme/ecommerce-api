from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from modules.order.domain.order_repository_interface import OrderRepository
from modules.order.infrastructure.order_model import Order, OrderItem

class OrderRepositoryImplementation(OrderRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def add_order_item(self, item: OrderItem) -> OrderItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_user_orders(self, user_id: UUID) -> List[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_order_by_id(self, order_id: UUID) -> Order:
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def update_order(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order