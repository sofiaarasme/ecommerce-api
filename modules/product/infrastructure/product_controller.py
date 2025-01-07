from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modules.product.application.product_service import ProductService
from modules.product.application.dtos.product_create_dto import ProductCreateDto
from modules.product.application.dtos.product_update_dto import ProductUpdateDto
from .product_repository import ProductRepositoryImplementation
from config import get_db

router = APIRouter()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repository = ProductRepositoryImplementation(db)
    return ProductService(repository)

@router.get("/")
async def read_products(service: ProductService = Depends(get_product_service)):
    return service.get_all_products()

@router.get("/{product_id}")
async def read_product(product_id: str, service: ProductService = Depends(get_product_service)):
    product = service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/")
async def create_product(
    product_data: ProductCreateDto,
    db: Session = Depends(get_db),
):
    repository = ProductRepositoryImplementation(db)
    service = ProductService(repository)
    return service.create_new_product(product_data.dict())

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product_data: ProductUpdateDto,
    db: Session = Depends(get_db),
):
    repository = ProductRepositoryImplementation(db)
    service = ProductService(repository)
    updated_product = service.update_product(product_id, product_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    repository = ProductRepositoryImplementation(db)
    service = ProductService(repository)
    deleted_product = service.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}