from pydantic import BaseModel
from typing import List
from uuid import UUID

class CartItemDto(BaseModel):
    cart_id: UUID
    product_id: UUID
    quantity: int

class CartCreateDto(BaseModel):
    items: List[CartItemDto]