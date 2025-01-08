from modules.order.domain.order_repository_interface import OrderRepository
from modules.carts.domain.cart_repository_interface import CartRepositoryInterface
from modules.user.infrastructure.user_model import User
from modules.order.infrastructure.order_model import Order, OrderItem
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