from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
from typing import Union
import uuid

SECRET_KEY = "12345678"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    for key, value in to_encode.items():
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token is invalid or expired",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
    except Exception:
        raise HTTPException(401, detail="Invalid token")
