import pytest
from pydantic import ValidationError
from modules.user.application.dtos.user_register_dto import UserCreateDto, RoleEnum

def test_user_create_dto_valid():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "role": RoleEnum.CUSTOMER
    }
    dto = UserCreateDto(**data)
    assert dto.username == "testuser"
    assert dto.email == "test@example.com"
    assert dto.password == "securepassword123"
    assert dto.role == RoleEnum.CUSTOMER

def test_user_create_dto_missing_username():
    data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "role": RoleEnum.CUSTOMER
    }
    with pytest.raises(ValidationError):
        UserCreateDto(**data)

def test_user_create_dto_missing_email():
    data = {
        "username": "testuser",
        "password": "securepassword123",
        "role": RoleEnum.CUSTOMER
    }
    with pytest.raises(ValidationError):
        UserCreateDto(**data)

def test_user_create_dto_missing_password():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "role": RoleEnum.CUSTOMER
    }
    with pytest.raises(ValidationError):
        UserCreateDto(**data)

def test_user_create_dto_missing_role():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    with pytest.raises(ValidationError):
        UserCreateDto(**data)
