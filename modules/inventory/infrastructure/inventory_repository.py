from uuid import UUID
from sqlalchemy.orm import Session
from modules.inventory.domain.inventory_repository_interface import InventoryRepository
from modules.inventory.infrastructure.inventory_model import InventoryModel

class InventoryRepositoryImplementation(InventoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_inventory(self, product_id: UUID) -> InventoryModel:
        inventory_model = self.db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
        if inventory_model:
            return InventoryModel(
                id=inventory_model.id,
                product_id=inventory_model.product_id,
                quantity=inventory_model.quantity,
                created_at=inventory_model.created_at,
                updated_at=inventory_model.updated_at
            )
        return None

    def save_inventory(self, inventory: InventoryModel) -> None:
        inventory_model = InventoryModel(
            id=inventory.id,
            product_id=inventory.product_id,
            quantity=inventory.quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at
        )
        self.db.add(inventory_model)
        self.db.commit()

    def update_inventory(self, inventory: InventoryModel) -> None:
        inventory_model = self.db.query(InventoryModel).filter(InventoryModel.id == inventory.id).first()
        if inventory_model:
            inventory_model.quantity = inventory.quantity
            inventory_model.updated_at = inventory.updated_at
            self.db.commit()