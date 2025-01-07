from pydantic import BaseModel

class ProductCreateDto(BaseModel):
    code: str
    name: str
    description: str
    price: float
    margin: float
    cost: float
    is_active: bool = True