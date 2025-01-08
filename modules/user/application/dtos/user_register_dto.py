from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    SUPERADMIN = 'superadmin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

class UserCreateDto(BaseModel):
    username: str
    email: str
    password: str  
    role: RoleEnum