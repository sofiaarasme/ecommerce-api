from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID
from modules.carts.application.cart_service import CartService
from modules.carts.infrastructure.car_model import Cart, CartItem
from .cart_repository import CartRepositoryImplementation
from config import get_db

router = APIRouter()

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
async def create_cart(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    repository = CartRepositoryImplementation(db)
    service = CartService(repository)
    db_cart = service.get_cart(data['user_id'])
    if db_cart:
        raise HTTPException(status_code=400, detail="Cart already exists")
    return service.create_cart(data)


@router.get("/")
async def read_cart(user_id: UUID, service: CartService = Depends(get_cart_service)):
    cart = service.get_cart(user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return serialize_cart(cart)

@router.post("/items")
async def add_cart_item(request: Request, cart_id: UUID, db: Session = Depends(get_db)):
    data = await request.json()
    item = CartItem(
        cart_id=cart_id,
        product_id=data['product_id'],
        quantity=data['quantity']
    )
    repository = CartRepositoryImplementation(db)
    service = CartService(repository)
    service.add_cart_item(cart_id, item)
    return serialize_cart_item(item)

@router.get("/items")
async def read_cart_items(cart_id: UUID, service: CartService = Depends(get_cart_service)):
    items = service.get_cart_items(cart_id)
    return [serialize_cart_item(item) for item in items]

@router.put("/items/{item_id}")
async def update_cart_item(item_id: UUID, quantity: int, db: Session = Depends(get_db)):
    repository = CartRepositoryImplementation(db)
    service = CartService(repository)
    updated_item = service.update_cart_item(item_id, quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return serialize_cart_item(updated_item)

@router.delete("/items/{item_id}")
async def delete_cart_item(item_id: UUID, db: Session = Depends(get_db)):
    repository = CartRepositoryImplementation(db)
    service = CartService(repository)
    deleted_item = service.delete_cart_item(item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart item deleted successfully"}
