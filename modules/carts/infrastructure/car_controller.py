from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from uuid import UUID
from modules.carts.application.cart_service import CartService
from modules.carts.application.dtos.create_cart_dto import CartItemDto
from modules.carts.application.dtos.cart_item_update_dto import CartItemUpdateDto
from modules.carts.infrastructure.car_model import Cart, CartItem
from .cart_repository import CartRepositoryImplementation
from modules.user.infrastructure.user_model import User
from modules.user.infrastructure.user_repository import UserRepositoryImplementation
from modules.user.application.user_service import UserService
from config import get_db
from fastapi.security import OAuth2PasswordBearer
from modules.user.infrastructure.jwt.auth import create_access_token, verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepositoryImplementation(db)
    return UserService(repository)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
):
    user_id = verify_token(token)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepositoryImplementation(db)
    return UserService(repository)

def get_cart_service(db: Session = Depends(get_db)) -> CartService:
    repository = CartRepositoryImplementation(db)
    return CartService(repository)

def serialize_cart(cart: Cart) -> dict:
    return {
        "id": str(cart.id),
        "user_id": str(cart.user_id),
        "created_at": cart.created_at.isoformat(),
        "updated_at": cart.updated_at.isoformat(),
        "items": [serialize_cart_item(item) for item in cart.items]
    }

def serialize_cart_item(item: CartItem) -> dict:
    return {
        "id": str(item.id),
        "cart_id": str(item.cart_id),
        "product_id": str(item.product_id),
        "quantity": item.quantity,
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat()
    }

@router.post("/")
async def create_cart(
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    return service.create_cart({}, current_user)

@router.post("/items")
async def add_cart_item(
    item_data: CartItemDto,
    service: CartService = Depends(get_cart_service)
):
    return service.add_cart_item(item_data.cart_id, item_data.dict())

@router.get("/")
async def read_cart(
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    cart = service.get_cart(current_user.id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return serialize_cart(cart)

@router.get("/items")
async def read_cart_items(cart_id: UUID, service: CartService = Depends(get_cart_service)):
    items = service.get_cart_items(cart_id)
    return [serialize_cart_item(item) for item in items]

@router.put("/items/{product_id}")
async def update_cart_item(
    item_data: CartItemUpdateDto,
    service: CartService = Depends(get_cart_service)
):
    updated_item = service.update_cart_item(item_data.product_id, item_data.quantity)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return serialize_cart_item(updated_item)

@router.delete("/items/{product_id}")
async def delete_cart_item(
    product_id: UUID,
    service: CartService = Depends(get_cart_service)
):
    service.delete_cart_item(product_id)
    return {"detail": "Item deleted"}
