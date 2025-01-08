from sqlalchemy.orm import Session
from sqlalchemy import func
from modules.order.infrastructure.order_model import Order, OrderItem, OrderStatus
from modules.product.infrastructure.product_model import Product
from modules.user.infrastructure.user_model import User
from typing import List, Dict
from uuid import UUID

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_total_sales(self) -> int:
        total_sales = self.db.query(func.count(Order.id)).filter(Order.status == OrderStatus.COMPLETED).scalar()
        return total_sales

    def get_sales_by_product(self, product_id: UUID) -> int:
        sales = self.db.query(func.count(OrderItem.id)).join(Order, OrderItem.order_id == Order.id).filter(Order.status == OrderStatus.COMPLETED, OrderItem.product_id == product_id).scalar()
        return sales

    def get_total_profit(self) -> float:
        total_profit = self.db.query(func.sum((Product.price - Product.cost) * OrderItem.quantity)).select_from(OrderItem).join(Product, OrderItem.product_id == Product.id).join(Order, OrderItem.order_id == Order.id).filter(Order.status == OrderStatus.COMPLETED).scalar()
        return total_profit

    def get_profit_by_product(self, product_id: UUID) -> float:
        profit = self.db.query(func.sum((Product.price - Product.cost) * OrderItem.quantity)).select_from(OrderItem).join(Product, OrderItem.product_id == Product.id).join(Order, OrderItem.order_id == Order.id).filter(Order.status == OrderStatus.COMPLETED, OrderItem.product_id == product_id).scalar()
        return profit

    def get_top_selling_products(self) -> List[Dict]:
        top_products = self.db.query(Product, func.sum(OrderItem.quantity).label('total_sold')).select_from(OrderItem).join(Product, OrderItem.product_id == Product.id).join(Order, OrderItem.order_id == Order.id).filter(Order.status == OrderStatus.COMPLETED).group_by(Product.id).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(10).all()
        return [{"product_id": str(product.id), "name": product.name, "total_sold": total_sold} for product, total_sold in top_products]

    def get_top_customers(self) -> List[Dict]:
        top_customers = self.db.query(User, func.count(Order.id).label('total_orders')).join(Order, Order.user_id == User.id).filter(Order.status == OrderStatus.COMPLETED).group_by(User.id).order_by(
            func.count(Order.id).desc()
        ).limit(10).all()
        return [{"user_id": str(user.id), "name": user.name, "total_orders": total_orders} for user, total_orders in top_customers]