from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from .inventory import InventoryInterface

class InventoryRepository(ABC):

    @abstractmethod
    def get_inventory(self, product_id: UUID) -> Optional[InventoryInterface]:
        pass

    @abstractmethod
    def save_inventory(self, inventory: InventoryInterface) -> None:
        pass

    @abstractmethod
    def update_inventory(self, inventory: InventoryInterface) -> None:
        pass