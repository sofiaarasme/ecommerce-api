from pydantic import BaseModel
from typing import Optional

class ProductUpdateDto(BaseModel):
    code: str = None
    name: str = None
    price: float = None
    cost: float = None
    margin: float = None
    description: str = None