from pydantic import BaseModel, ConfigDict
from modules.order.infrastructure.order_model import OrderStatus
from uuid import UUID

class UpdateOrderDto(BaseModel):
    order_id: UUID
    status: OrderStatus 
    
    class Config:
        arbitrary_types_allowed = True 