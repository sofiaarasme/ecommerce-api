from abc import ABC, abstractmethod
from typing import List
from .user import UserInterface

class UserRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[UserInterface]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> UserInterface:
        pass

    @abstractmethod
    def register(self, user: UserInterface) -> UserInterface:
        pass