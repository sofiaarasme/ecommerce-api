import pytest
from pydantic import ValidationError
from modules.inventory.application.dtos.inventory_create_dto import InventoryCreateDto

class TestInventoryCreateDto:

    def test_valid_quantity(self):
        dto = InventoryCreateDto(quantity=10)
        assert dto.quantity == 10

    def test_invalid_quantity_type(self):
        with pytest.raises(ValidationError):
            InventoryCreateDto(quantity='ten')  # Usar un valor no convertible a int para asegurar la falla

    def test_missing_quantity(self):
        with pytest.raises(ValidationError):
            InventoryCreateDto()  # Falta el campo quantity
