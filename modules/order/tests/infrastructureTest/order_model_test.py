import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.user.infrastructure.user_model import User, Role
from modules.order.infrastructure.order_model import Order, OrderItem, OrderStatus
from config import Base
from uuid import uuid4
from datetime import datetime

# Configuración de la base de datos en memoria para pruebas
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def session_factory(engine, tables):
    return sessionmaker(bind=engine)

@pytest.fixture(scope='function')
def session(session_factory):
    session = session_factory()
    yield session
    session.rollback()
    session.close()

def test_create_order(session):
    user_id = uuid4()
    unique_username = f"testuser{uuid4()}"
    unique_email = f"{unique_username}@example.com"
    user = User(id=user_id, username=unique_username, email=unique_email, role=Role.CUSTOMER.value)
    session.add(user)
    session.commit()
    
    order = Order(user_id=user_id, total_amount=100.0, status=OrderStatus.PENDING)
    session.add(order)
    session.commit()
    
    assert order.id is not None
    assert order.user_id == user_id
    assert order.total_amount == 100.0
    assert order.status == OrderStatus.PENDING
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)
    assert order.items == []

def test_add_order_item(session):
    user_id = uuid4()
    unique_username = f"testuser{uuid4()}"
    unique_email = f"{unique_username}@example.com"
    user = User(id=user_id, username=unique_username, email=unique_email, role=Role.CUSTOMER.value)
    session.add(user)
    session.commit()
    
    order = Order(user_id=user_id, total_amount=100.0, status=OrderStatus.PENDING)
    session.add(order)
    session.commit()
    
    product_id = uuid4()
    order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=3)
    session.add(order_item)
    session.commit()
    
    assert order_item.id is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == product_id
    assert order_item.quantity == 3
    assert isinstance(order_item.created_at, datetime)
    assert isinstance(order_item.updated_at, datetime)
    assert order_item in order.items
