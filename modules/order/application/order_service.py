from modules.order.domain.order_repository_interface import OrderRepository
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface
from modules.user.infrastructure.user_model import User, Role
from modules.order.infrastructure.order_model import Order, OrderItem, OrderStatus
from uuid import UUID

class OrderService:
    def __init__(self, order_repository: OrderRepository, cart_repository: CartRepositoryInterface):
        self.order_repository = order_repository
        self.cart_repository = cart_repository

    def create_order_from_cart(self, current_user: User):
        cart = self.cart_repository.get_cart(current_user.id)
        if not cart or not cart.items:
            raise ValueError("Cart is empty or does not exist")

        total_amount = sum(item.product.price * item.quantity for item in cart.items)
        order_data = {
            'user_id': current_user.id,
            'total_amount': total_amount,
            'status': 'pending'
        }
        new_order = Order(**order_data)
        self.order_repository.create_order(new_order)
        
        for cart_item in cart.items:
            item_data = {
                'order_id': new_order.id,
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity
            }
            new_item = OrderItem(**item_data)
            self.order_repository.add_order_item(new_item)
        
        return {"Order Created Succesfully"}

    def get_user_orders(self, user_id: UUID):
        return self.order_repository.get_user_orders(user_id)

    def get_order_by_id(self, order_id: UUID):
        return self.order_repository.get_order_by_id(order_id)
    
    def update_order_status(self, order_id: UUID, status: OrderStatus, current_user: User):
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        if current_user.role != Role.MANAGER:
            raise ValueError("Only managers can update order status")

        order.status = status
        self.order_repository.update_order(order)
        return order

    def cancel_order(self, order_id: UUID, current_user: User):
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        
        if current_user.role == Role.CUSTOMER and order.user_id != current_user.id:
            raise ValueError("Customers can only cancel their own orders")
        
        if current_user.role == Role.CUSTOMER and order.status != OrderStatus.PENDING:
            raise ValueError("Customers can only cancel pending orders")

        order.status = OrderStatus.CANCELLED
        self.order_repository.update_order(order)
        return order