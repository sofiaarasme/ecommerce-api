import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.carts.infrastructure.car_model import Cart, CartItem
from modules.user.infrastructure.user_model import User, Role  # Asegúrate de importar Role
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

def test_create_cart(session):
    user_id = uuid4()
    unique_username = f"testuser{uuid4()}"
    unique_email = f"{unique_username}@example.com"
    user = User(id=user_id, username=unique_username, email=unique_email, role=Role.CUSTOMER.value)  # Proporciona un nombre de usuario y correo únicos
    session.add(user)
    session.commit()
    
    cart = Cart(user_id=user_id)
    session.add(cart)
    session.commit()
    
    assert cart.id is not None
    assert cart.user_id == user_id
    assert isinstance(cart.created_at, datetime)
    assert isinstance(cart.updated_at, datetime)
    assert cart.items == []

def test_add_cart_item(session):
    user_id = uuid4()
    unique_username = f"testuser{uuid4()}"
    unique_email = f"{unique_username}@example.com"
    user = User(id=user_id, username=unique_username, email=unique_email, role=Role.CUSTOMER.value)  # Proporciona un nombre de usuario y correo únicos
    session.add(user)
    session.commit()
    
    cart = Cart(user_id=user_id)
    session.add(cart)
    session.commit()
    
    product_id = uuid4()
    cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=3)
    session.add(cart_item)
    session.commit()
    
    assert cart_item.id is not None
    assert cart_item.cart_id == cart.id
    assert cart_item.product_id == product_id
    assert cart_item.quantity == 3
    assert isinstance(cart_item.created_at, datetime)
    assert isinstance(cart_item.updated_at, datetime)
    assert cart_item in cart.items
