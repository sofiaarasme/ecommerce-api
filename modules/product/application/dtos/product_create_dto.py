from pydantic import BaseModel

class ProductCreateDto(BaseModel):
    name: str
    description: str
    price: int
    is_active: bool = True