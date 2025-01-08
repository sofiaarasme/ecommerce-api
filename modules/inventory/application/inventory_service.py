from uuid import UUID
from typing import Optional
from datetime import datetime
import uuid 
from modules.inventory.domain.inventory_repository_interface import InventoryRepository
from modules.inventory.infrastructure.inventory_model import InventoryModel

class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def get_inventory(self, product_id: UUID) -> Optional[InventoryModel]:
        return self.inventory_repository.get_inventory(product_id)

    def update_inventory(self, product_id: UUID, quantity: int) -> InventoryModel:
        inventory = self.inventory_repository.get_inventory(product_id)
        
        if inventory is None:
            raise ValueError("Inventory not found")

        inventory.quantity = quantity
        inventory.updated_at = datetime.utcnow()
        
        self.inventory_repository.update_inventory(inventory)
        
        return inventory

    def add_to_inventory(self, product_id: UUID, quantity: int) -> InventoryModel:
        inventory = self.inventory_repository.get_inventory(product_id)

        if inventory is None:
            inventory = InventoryModel(
                id=uuid.uuid4(),
                product_id=product_id,
                quantity=quantity,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.inventory_repository.save_inventory(inventory)
        else:
            inventory.quantity += quantity
            inventory.updated_at = datetime.utcnow()
            self.inventory_repository.update_inventory(inventory)
        
        return inventory
