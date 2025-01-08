from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime

class Role(Enum):
    SUPERADMIN = 'superadmin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

class UserInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def username(self) -> str:
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @property
    @abstractmethod
    def hashed_password(self) -> str:
        pass
    
    @property
    @abstractmethod
    def role(self) -> Role:
        pass

    @property
    @abstractmethod
    def created_at(self) -> str:
        pass

    @property
    @abstractmethod
    def updated_at(self) -> str:
        pass

class UserConcrete(UserInterface):
    def __init__(self, username: str, email: str, hashed_password: str, role: Role):
        self._id = uuid4()
        self._username = username
        self._email = email
        self._hashed_password = hashed_password
        self._role = role
        self._created_at = datetime.utcnow().isoformat()
        self._updated_at = datetime.utcnow().isoformat()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def role(self) -> Role:
        return self._role

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at
