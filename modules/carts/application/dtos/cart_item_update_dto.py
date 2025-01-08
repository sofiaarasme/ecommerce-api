from pydantic import BaseModel
from uuid import UUID

class CartItemUpdateDto(BaseModel):
    product_id: UUID
    quantity: int