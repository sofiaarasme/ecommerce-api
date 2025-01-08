import pytest
from uuid import UUID
from modules.user.tests.domainTest.user_interface import UserConcrete, Role 

def test_user_concrete_initialization():
    user = UserConcrete(username="testuser", email="test@example.com", hashed_password="hashed_password", role=Role.CUSTOMER)
    assert isinstance(user.id, UUID)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.role == Role.CUSTOMER
    assert isinstance(user.created_at, str)
    assert isinstance(user.updated_at, str)

def test_user_concrete_role_enum():
    user = UserConcrete(username="testuser", email="test@example.com", hashed_password="hashed_password", role=Role.MANAGER)
    assert user.role == Role.MANAGER

def test_user_concrete_id_unique():
    user1 = UserConcrete(username="user1", email="user1@example.com", hashed_password="password1", role=Role.CUSTOMER)
    user2 = UserConcrete(username="user2", email="user2@example.com", hashed_password="password2", role=Role.MANAGER)
    assert user1.id != user2.id
