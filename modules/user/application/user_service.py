from typing import List
from modules.user.infrastructure.user_model import User
from modules.user.domain.user_repository_interface import UserRepository

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self) -> List[User]:
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.repository.get_by_id(user_id)

    def register_new_user(self, user_data: dict):
        new_user = User(**user_data)
        return self.repository.register(new_user)