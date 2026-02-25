import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
def ac():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

@pytest.mark.asyncio
async def test_erase_all_products(ac):
    async with ac:
        response = await ac.delete("/api/products/erase")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_all_products_empty(ac):
    async with ac:
        await ac.delete("/api/products/erase")
        response = await ac.get("/api/products")
    assert response.status_code == 200
    assert response.json()["data"] == []

@pytest.mark.asyncio
async def test_create_product(ac):
    async with ac:
        await ac.delete("/api/products/erase")
        payload = {
            "id": "MLB1",
            "title": "Product 1",
            "price": 10.0,
            "currency_id": "BRL",
            "available_quantity": 1,
            "thumbnail": "",
            "condition": "new",
            "category_id": "CAT1"
        }
        response = await ac.post("/api/products", json=payload)
    assert response.status_code == 201
    assert response.json()["data"]["id"] == "MLB1"

@pytest.mark.asyncio
async def test_create_product_duplicate(ac):
    async with ac:
        payload = {
            "id": "MLB1",
            "title": "Product 1",
            "price": 10.0,
            "category_id": "CAT1"
        }
        response = await ac.post("/api/products", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["message"]

@pytest.mark.asyncio
async def test_create_multiple_and_get(ac):
    payloads = [
        {"id": "MLB2", "title": "Product 2", "price": 20.0, "category_id": "CAT2"},
        {"id": "MLB3", "title": "Product 3", "price": 30.0, "category_id": "CAT3"}
    ]
    async with ac:
        for p in payloads:
            response = await ac.post("/api/products", json=p)
            assert response.status_code == 201
        
        response = await ac.get("/api/products")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 3
    ids = [product["id"] for product in data]
    assert sorted(ids) == ["MLB1", "MLB2", "MLB3"]

@pytest.mark.asyncio
async def test_delete_by_id(ac):
    async with ac:
        response = await ac.delete("/api/products/MLB2")
        assert response.status_code == 200
        
        response = await ac.get("/api/products/MLB2")
        assert response.status_code == 404
        
        response = await ac.get("/api/products")
    data = response.json()["data"]
    assert len(data) == 2
    ids = [product["id"] for product in data]
    assert "MLB2" not in ids

@pytest.mark.asyncio
async def test_get_product_not_found(ac):
    async with ac:
        response = await ac.get("/api/products/NONEXISTENT")
    assert response.status_code == 404
    assert "not found" in response.json()["message"]

@pytest.mark.asyncio
async def test_get_product_by_id(ac):
    async with ac:
        response = await ac.get("/api/products/MLB1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == "MLB1"
    assert response.json()["data"]["title"] == "Product 1"
