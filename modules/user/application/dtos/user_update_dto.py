from pydantic import BaseModel, root_validator
from enum import Enum

class Role(str, Enum):
    SUPERADMIN = 'superadmin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

class UserUpdateDto(BaseModel):
    username: str = None
    email: str = None
    password: str = None
    role: Role
    
    @root_validator(pre=True)
    def set_default_role(cls, values):
        if 'role' not in values:
            values['role'] = Role.MANAGER
        return values
        
    
    class Config:
        orm_mode = True