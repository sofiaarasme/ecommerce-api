from pydantic import BaseModel

class ProductResponseDto(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_active: bool

    class Config:
        from_attributes = True