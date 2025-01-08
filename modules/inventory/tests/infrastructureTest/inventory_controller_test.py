""" import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app

class TestInventoryAPI:

    @pytest.fixture(scope="class")
    def client(self):
        with TestClient(app) as c:
            yield c

    def test_get_inventory_not_found(self, client):
        product_id = uuid4()
        response = client.get(f"/{product_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Inventory not found"}

    def test_get_inventory(self, client):
        product_id = uuid4()
        client.post(f"/{product_id}", json={"quantity": 10})
        response = client.get(f"/{product_id}")
        assert response.status_code == 200
        assert "product_id" in response.json()
        assert "quantity" in response.json()

    def test_update_inventory_not_found(self, client):
        product_id = uuid4()
        response = client.put(f"/{product_id}", json={"quantity": 20})
        assert response.status_code == 404
        assert response.json() == {"detail": "Inventory not found"}

    def test_add_to_inventory(self, client):
        product_id = uuid4()
        response = client.post(f"/{product_id}", json={"quantity": 10})
        assert response.status_code == 200
        assert "product_id" in response.json()
        assert "quantity" in response.json()
        assert response.json()["quantity"] == 10

    def test_update_inventory(self, client):
        product_id = uuid4()
        client.post(f"/{product_id}", json={"quantity": 10})
        response = client.put(f"/{product_id}", json={"quantity": 20})
        assert response.status_code == 200
        assert "product_id" in response.json()
        assert "quantity" in response.json()
        assert response.json()["quantity"] == 20
 """