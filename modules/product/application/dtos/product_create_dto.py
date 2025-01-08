from pydantic import BaseModel, Field, validator

class ProductCreateDto(BaseModel):
    code: str
    name: str
    description: str
    margin: float = Field(..., gt=0, lt=1, description="Margin should be a value between 0 and 1")
    cost: float
    is_active: bool = True
    price: float = None
    
    @validator('price', pre=True, always=True)
    def calculate_price(cls, v, values):
        cost = values.get('cost')
        margin = values.get('margin')
        if cost is not None and margin is not None:
            return cost / (1 - margin)
        return v