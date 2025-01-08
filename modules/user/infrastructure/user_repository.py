from sqlalchemy.orm import Session
from typing import List
from modules.user.infrastructure.user_model import User
from modules.user.domain.user_repository_interface import UserRepository

class UserRepositoryImplementation(UserRepository):
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def register(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user