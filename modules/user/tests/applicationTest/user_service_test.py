import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from modules.user.infrastructure.user_model import User, Role
from modules.user.application.user_service import UserService
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def user_service(mock_repository):
    return UserService(repository=mock_repository)

def test_get_all_users(user_service, mock_repository):
    mock_users = [User(id=1, username="user1", email="user1@example.com"), User(id=2, username="user2", email="user2@example.com")]
    mock_repository.get_all.return_value = mock_users
    users = user_service.get_all_users()
    assert users == mock_users

def test_get_user_by_id(user_service, mock_repository):
    mock_user = User(id=1, username="testuser", email="test@example.com")
    mock_repository.get_by_id.return_value = mock_user
    user = user_service.get_user_by_id(1)
    assert user == mock_user

def test_get_user_by_email(user_service, mock_repository):
    mock_user = User(id=1, username="testuser", email="test@example.com")
    mock_repository.get_by_email.return_value = mock_user
    user = user_service.get_user_by_email("test@example.com")
    assert user == mock_user

def test_register_new_user(user_service, mock_repository):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "role": Role.CUSTOMER.value
    }
    hashed_password = pwd_context.hash(user_data["password"])
    expected_user = User(id=1, username="testuser", email="test@example.com", hashed_password=hashed_password, role=Role.CUSTOMER.value)
    mock_repository.register.return_value = expected_user
    new_user = user_service.register_new_user(user_data)
    assert new_user.id is not None
    assert new_user.email == "test@example.com"
    assert pwd_context.verify("securepassword123", new_user.hashed_password)
    assert new_user.role == Role.CUSTOMER.value

def test_get_users_by_role(user_service, mock_repository):
    mock_users = [User(id=1, username="user1", email="user1@example.com", role=Role.CUSTOMER.value)]
    mock_repository.get_by_role.return_value = mock_users
    users = user_service.get_users_by_role(Role.CUSTOMER.value)
    assert users == mock_users

def test_update_user(user_service, mock_repository):
    user_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "newpassword",
        "role": Role.MANAGER.value
    }
    hashed_password = pwd_context.hash(user_data["password"])
    current_user = User(id=1, username="currentuser", email="current@example.com", hashed_password="oldpassword")
    updated_user = User(id=1, username="updateduser", email="updated@example.com", hashed_password=hashed_password, role=Role.MANAGER.value)
    
    mock_repository.get_by_id.return_value = current_user
    mock_repository.update.return_value = updated_user
    
    user_data["hashed_password"] = hashed_password
    user_data.pop("password") 
    
    user = user_service.update_user(1, user_data, current_user)
    
    assert user.id == updated_user.id
    assert user.username == updated_user.username
    assert user.email == updated_user.email
    assert pwd_context.verify("newpassword", user.hashed_password)
    assert user.role == updated_user.role


def test_update_user_not_found(user_service, mock_repository):
    current_user = User(id=1, username="currentuser", email="current@example.com")
    mock_repository.get_by_id.return_value = None
    user_data = {"username": "updateduser"}

    with pytest.raises(HTTPException) as excinfo:
        user_service.update_user(1, user_data, current_user)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "User not found"

def test_delete_user(user_service, mock_repository):
    mock_user = User(id=1, username="testuser", email="test@example.com")
    mock_repository.get_by_id.return_value = mock_user
    user_service.delete_user(1)
    mock_repository.delete.assert_called_once_with(mock_user)

def test_authenticate_user(user_service, mock_repository):
    password = "securepassword123"
    hashed_password = pwd_context.hash(password)
    mock_user = User(id=1, username="testuser", email="test@example.com", hashed_password=hashed_password)
    mock_repository.get_by_email.return_value = mock_user

    user = user_service.authenticate_user("test@example.com", password)
    assert user == mock_user

def test_authenticate_user_invalid_password(user_service, mock_repository):
    password = "securepassword123"
    wrong_password = "wrongpassword"
    hashed_password = pwd_context.hash(password)
    mock_user = User(id=1, username="testuser", email="test@example.com", hashed_password=hashed_password)
    mock_repository.get_by_email.return_value = mock_user

    user = user_service.authenticate_user("test@example.com", wrong_password)
    assert user is None
