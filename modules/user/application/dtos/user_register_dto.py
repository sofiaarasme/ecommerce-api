from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    SUPERADMIN = 'superadmin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

class UserCreateDto(BaseModel):
    username: str
    email: str
    hashed_password: str  
    role: RoleEnum