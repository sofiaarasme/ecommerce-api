import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime
from modules.inventory.application.inventory_service import InventoryService
from modules.inventory.domain.inventory_repository_interface import InventoryRepository
from modules.inventory.infrastructure.inventory_model import InventoryModel

class TestInventoryService:

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.mock_repository = MagicMock(spec=InventoryRepository)
        self.inventory_service = InventoryService(self.mock_repository)

    def test_get_inventory(self):
        product_id = uuid4()
        inventory = InventoryModel(
            id=uuid4(),
            product_id=product_id,
            quantity=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.mock_repository.get_inventory.return_value = inventory

        result = self.inventory_service.get_inventory(product_id)
        assert result == inventory
        self.mock_repository.get_inventory.assert_called_once_with(product_id)

    def test_update_inventory(self):
        product_id = uuid4()
        inventory = InventoryModel(
            id=uuid4(),
            product_id=product_id,
            quantity=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.mock_repository.get_inventory.return_value = inventory

        updated_inventory = self.inventory_service.update_inventory(product_id, 20)
        assert updated_inventory.quantity == 20
        assert updated_inventory.updated_at <= datetime.utcnow()
        self.mock_repository.update_inventory.assert_called_once_with(updated_inventory)

    def test_update_inventory_not_found(self):
        product_id = uuid4()
        self.mock_repository.get_inventory.return_value = None

        with pytest.raises(ValueError):
            self.inventory_service.update_inventory(product_id, 20)

    def test_add_to_inventory_new(self):
        product_id = uuid4()
        self.mock_repository.get_inventory.return_value = None

        new_inventory = self.inventory_service.add_to_inventory(product_id, 10)
        assert new_inventory.product_id == product_id
        assert new_inventory.quantity == 10
        assert new_inventory.created_at <= datetime.utcnow()
        assert new_inventory.updated_at <= datetime.utcnow()
        self.mock_repository.save_inventory.assert_called_once_with(new_inventory)

    def test_add_to_inventory_existing(self):
        product_id = uuid4()
        inventory = InventoryModel(
            id=uuid4(),
            product_id=product_id,
            quantity=10,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.mock_repository.get_inventory.return_value = inventory

        updated_inventory = self.inventory_service.add_to_inventory(product_id, 5)
        assert updated_inventory.quantity == 15
        assert updated_inventory.updated_at <= datetime.utcnow()
        self.mock_repository.update_inventory.assert_called_once_with(updated_inventory)
