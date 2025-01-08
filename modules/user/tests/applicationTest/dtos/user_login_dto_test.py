import pytest
from pydantic import ValidationError
from modules.user.application.dtos.user_login_dto import UserLoginDto 

def test_user_login_dto_valid():
    data = {"email": "test@example.com", "password": "securepassword123"}
    dto = UserLoginDto(**data)
    assert dto.email == "test@example.com"
    assert dto.password == "securepassword123"

def test_user_login_dto_missing_email():
    data = {"password": "securepassword123"}
    with pytest.raises(ValidationError):
        UserLoginDto(**data)

def test_user_login_dto_missing_password():
    data = {"email": "test@example.com"}
    with pytest.raises(ValidationError):
        UserLoginDto(**data)
