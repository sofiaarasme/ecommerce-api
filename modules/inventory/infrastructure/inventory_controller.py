from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from modules.inventory.application.inventory_service import InventoryService
from .inventory_repository import InventoryRepositoryImplementation
from modules.inventory.application.dtos.inventory_create_dto import InventoryCreateDto
from config import get_db

router = APIRouter()

def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
    repository = InventoryRepositoryImplementation(db)
    return InventoryService(repository)

@router.get("/{product_id}")
async def get_inventory(product_id: UUID, inventory_service: InventoryService = Depends(get_inventory_service)):
    inventory = inventory_service.get_inventory(product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return {"product_id": inventory.product_id, "quantity": inventory.quantity}

@router.put("/{product_id}")
def update_inventory(
    product_id: UUID, 
    inventory_data: InventoryCreateDto,
    inventory_service: InventoryService = Depends(get_inventory_service)
):
    try:
        inventory = inventory_service.update_inventory(product_id, inventory_data.quantity)
        return {"product_id": inventory.product_id, "quantity": inventory.quantity}
    except ValueError:
        raise HTTPException(status_code=404, detail="Inventory not found")

@router.post("/{product_id}")
def add_to_inventory(
    product_id: UUID, 
    inventory_data: InventoryCreateDto,
    inventory_service: InventoryService = Depends(get_inventory_service)
):
    inventory = inventory_service.add_to_inventory(product_id, inventory_data.quantity)
    return {"product_id": inventory.product_id, "quantity": inventory.quantity}