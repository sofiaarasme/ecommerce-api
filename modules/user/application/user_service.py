from typing import List
from modules.user.infrastructure.user_model import User
from modules.user.domain.user_repository_interface import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self) -> List[User]:
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> User:
        return self.repository.get_by_email(email)

    def register_new_user(self, user_data: dict)-> User:
        user_data['hashed_password'] = pwd_context.hash(user_data.pop('password'))
        user_data['role'] = user_data['role'].value
        new_user = User(**user_data)
        return self.repository.register(new_user)
    
    def get_users_by_role(self, role: str) -> List[User]:
        return self.repository.get_by_role(role)

    def update_user(self, user_id: int, user_data: dict) -> User:
        user = self.get_user_by_id(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        return self.repository.update(user)

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        return self.repository.delete(user)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user