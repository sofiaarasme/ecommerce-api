import pytest
from uuid import uuid4, UUID
from datetime import datetime
from abc import ABC, abstractmethod

class InventoryInterface(ABC):

    @property
    @abstractmethod
    def id(self) -> UUID:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass

    @property
    @abstractmethod
    def product_id(self) -> UUID:
        pass
    
    @property
    @abstractmethod
    def created_at(self) -> str:
        pass

    @property
    @abstractmethod
    def updated_at(self) -> str:
        pass

class InventoryImplementation(InventoryInterface):
    def __init__(self, id: UUID, product_id: UUID, quantity: int, created_at: str, updated_at: str):
        self._id = id
        self._product_id = product_id
        self._quantity = quantity
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def product_id(self) -> UUID:
        return self._product_id
    
    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

class TestInventoryInterface:

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.inventory = InventoryImplementation(
            id=uuid4(),
            product_id=uuid4(),
            quantity=10,
            created_at=str(datetime.utcnow()),
            updated_at=str(datetime.utcnow())
        )

    def test_id(self):
        assert isinstance(self.inventory.id, UUID)

    def test_quantity(self):
        assert isinstance(self.inventory.quantity, int)
        assert self.inventory.quantity == 10

    def test_product_id(self):
        assert isinstance(self.inventory.product_id, UUID)

    def test_created_at(self):
        assert isinstance(self.inventory.created_at, str)

    def test_updated_at(self):
        assert isinstance(self.inventory.updated_at, str)
