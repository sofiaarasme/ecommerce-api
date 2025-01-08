from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from config import Base

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("CartItem", back_populates="cart")
    user = relationship("User", back_populates="cart")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('carts.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")