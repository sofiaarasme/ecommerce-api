from pydantic import BaseModel
from typing import List
from uuid import UUID

class OrderItemDto(BaseModel):
    product_id: UUID
    quantity: int

class OrderCreateDto(BaseModel):
    items: List[OrderItemDto]