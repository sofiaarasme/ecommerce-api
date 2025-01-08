from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.user.application.user_service import UserService
from modules.user.application.dtos.user_register_dto import UserCreateDto
from modules.user.infrastructure.user_repository import UserRepositoryImplementation
from config import get_db

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepositoryImplementation(db)
    return UserService(repository)

@router.get("/")
async def read_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.post("/register")
async def register_user(
    user_data: UserCreateDto,
    db: Session = Depends(get_db),
):
    repository = UserRepositoryImplementation(db)
    service = UserService(repository)
    return service.register_new_user(user_data.dict())
