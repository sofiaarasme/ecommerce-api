from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from config import Base
from datetime import datetime
from enum import Enum as PyEnum

class Role(PyEnum):
    SUPERADMIN = 'superadmin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), index=True, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)