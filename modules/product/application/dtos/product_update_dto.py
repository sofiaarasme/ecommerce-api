from pydantic import BaseModel
from typing import Optional

class ProductUpdateDto(BaseModel):
    name: str = None
    price: float= None
    description: str = None