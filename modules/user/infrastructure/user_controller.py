from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.user.application.user_service import UserService
from modules.user.application.dtos.user_register_dto import UserCreateDto
from modules.user.application.dtos.user_login_dto import UserLoginDto
from modules.user.application.dtos.user_update_dto import UserUpdateDto
from modules.user.infrastructure.user_model import User, Role
from modules.user.infrastructure.user_repository import UserRepositoryImplementation
from config import get_db
from fastapi.security import OAuth2PasswordBearer
from modules.user.infrastructure.jwt.auth import create_access_token, verify_token


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepositoryImplementation(db)
    return UserService(repository)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
):
    user_id = verify_token(token)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def get_superadmin_user(current_user=Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/")
async def read_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.post("/register")
async def register_user(
    user_data: UserCreateDto,
    db: Session = Depends(get_db),
):
    try:
        user_service = UserService(repository=UserRepositoryImplementation(db))   
        created_user = user_service.register_new_user(user_data.dict())
        return {"message": "User registered successfully", "user": created_user}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/create_superadmin")
async def create_superadmin(
    user_data: UserCreateDto,
    db: Session = Depends(get_db),
):
    try:
        user_service = UserService(repository=UserRepositoryImplementation(db))
        
        existing_superadmin = user_service.get_users_by_role(Role.SUPERADMIN.value)
        
        if existing_superadmin:
            raise HTTPException(status_code=400, detail="A superadmin already exists. Cannot create another one.")
        
        else:
            user_data_dict = user_data.dict()
            user_data_dict['role'] = "superadmin"
            created_superadmin = user_service.register_new_user(user_data_dict)

            return {"message": "Superadmin created successfully", "user": created_superadmin}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/managers")
async def create_manager(
    user_data: UserCreateDto,
    current_user=Depends(get_superadmin_user),
    service: UserService = Depends(get_user_service)
):
    user_data.role = Role.MANAGER.value

    return service.register_new_user(user_data.dict())

@router.get("/managers")
async def get_managers(
    current_user=Depends(get_superadmin_user),
    service: UserService = Depends(get_user_service)
):
    return service.get_users_by_role("manager")

@router.put("/managers/{manager_id}")
async def update_manager(
    manager_id: str,
    user_data: UserUpdateDto,
    current_user=Depends(get_superadmin_user),
    service: UserService = Depends(get_user_service)
):
    manager = service.get_user_by_id(manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    return service.update_user(manager_id, user_data.dict())

@router.delete("/managers/{manager_id}")
async def delete_manager(
    manager_id: str,
    current_user=Depends(get_superadmin_user),
    service: UserService = Depends(get_user_service)
):
    manager = service.get_user_by_id(manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    else:
        service.delete_user(manager_id)

    return "Manager deleted"

@router.post("/login")
async def login_for_access_token(
    user_data: UserLoginDto,
    service: UserService = Depends(get_user_service)
):
    user = service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_data: UserUpdateDto,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    return service.update_user(user_id, user_data.dict(), current_user)