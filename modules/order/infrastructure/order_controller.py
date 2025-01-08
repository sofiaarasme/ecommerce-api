from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from modules.order.application.dtos.create_order_dto import OrderCreateDto
from modules.order.application.order_service import OrderService
from modules.user.infrastructure.user_controller import get_current_user
from modules.order.infrastructure.order_repository import OrderRepositoryImplementation
from modules.carts.infrastructure.cart_repository import CartRepositoryImplementation
from modules.user.infrastructure.user_model import User
from modules.order.infrastructure.order_model import Order, OrderItem
from modules.order.application.dtos.update_order_dto import UpdateOrderDto
from config import get_db

router = APIRouter()

def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    order_repository = OrderRepositoryImplementation(db)
    cart_repository = CartRepositoryImplementation(db)
    return OrderService(order_repository, cart_repository)

@router.post("/")
async def create_order(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    try:
        return service.create_order_from_cart(current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    orders = service.get_user_orders(current_user.id)
    return [serialize_order(order) for order in orders]

@router.get("/{order_id}")
async def get_order_by_id(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    order = service.get_order_by_id(order_id)
    if order is None or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return serialize_order(order)

@router.put("/{order_id}/status")
async def update_order_status(
    update_data: UpdateOrderDto, 
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    try:
        return serialize_order(service.update_order_status(update_data.order_id, update_data.status, current_user))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{order_id}/cancel")
async def cancel_order(
    update_data: UpdateOrderDto, 
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    try:
        return serialize_order(service.cancel_order(update_data.order_id, current_user))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def serialize_order(order: Order) -> dict:
    return {
        "id": str(order.id),
        "user_id": str(order.user_id),
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
        "total_amount": order.total_amount,
        "status": order.status,
        "items": [serialize_order_item(item) for item in order.items]
    }

def serialize_order_item(item: OrderItem) -> dict:
    return {
        "id": str(item.id),
        "order_id": str(item.order_id),
        "product_id": str(item.product_id),
        "quantity": item.quantity,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat()
    }