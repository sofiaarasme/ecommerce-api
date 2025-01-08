from pydantic import BaseModel

class InventoryCreateDto(BaseModel):
    quantity: int