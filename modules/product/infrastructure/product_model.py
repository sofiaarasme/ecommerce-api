from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from config import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String, index=True)
    description = Column(String)
    cost = Column(Float)
    margin = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow) 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    inventory = relationship("InventoryModel", back_populates="product")