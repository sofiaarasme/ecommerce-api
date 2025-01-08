import pytest
from pydantic import ValidationError
from modules.user.application.dtos.user_update_dto import UserUpdateDto, Role

def test_user_update_dto_with_all_fields():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "role": Role.SUPERADMIN
    }
    dto = UserUpdateDto(**data)
    assert dto.username == "testuser"
    assert dto.email == "test@example.com"
    assert dto.password == "securepassword123"
    assert dto.role == Role.SUPERADMIN

def test_user_update_dto_with_missing_role():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    dto = UserUpdateDto(**data)
    assert dto.username == "testuser"
    assert dto.email == "test@example.com"
    assert dto.password == "securepassword123"
    assert dto.role == Role.MANAGER  # Default role should be MANAGER

def test_user_update_dto_with_partial_data():
    data = {
        "username": "testuser"
    }
    dto = UserUpdateDto(**data)
    assert dto.username == "testuser"
    assert dto.email is None
    assert dto.password is None
    assert dto.role == Role.MANAGER  # Default role should be MANAGER

def test_user_update_dto_invalid_role():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
        "role": "invalidrole"  # Invalid role
    }
    with pytest.raises(ValidationError):
        UserUpdateDto(**data)
