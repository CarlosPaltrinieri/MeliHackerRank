import pytest
from unittest.mock import Mock, AsyncMock
from sqlalchemy.orm import Session
from app.services.product_service import ProductService
from app.domain.models import Product, Category, ProductDescription
from app.domain.schemas import ProductCreateSchema

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)

@pytest.mark.asyncio
async def test_create_product_success(mock_repository, mock_db_session):
    mock_repository.get_product_with_details = AsyncMock(return_value=None)
    
    mock_product = Product(id="MLB1", title="Test Product", price=100.0, category_id="CAT1", currency_id="BRL", available_quantity=10, thumbnail="", condition="new")
    mock_repository.create = AsyncMock(return_value=mock_product)
    
    service = ProductService(repository=mock_repository)
    schema = ProductCreateSchema(id="MLB1", title="Test Product", price=100.0, category_id="CAT1")
    
    result = await service.create_product(mock_db_session, schema)
    
    assert result.status_code == 201
    assert result.data.id == "MLB1"

@pytest.mark.asyncio
async def test_create_product_duplicate(mock_repository, mock_db_session):
    mock_product = Product(id="MLB1", title="Test Product", price=100.0, category_id="CAT1", currency_id="BRL", available_quantity=10, thumbnail="", condition="new")
    mock_repository.get_product_with_details = AsyncMock(return_value=mock_product)
    
    service = ProductService(repository=mock_repository)
    schema = ProductCreateSchema(id="MLB1", title="Test Product", price=100.0, category_id="CAT1")
    
    result = await service.create_product(mock_db_session, schema)
    
    assert result.status_code == 400
    assert "already exists" in result.message

@pytest.mark.asyncio
async def test_get_all_products(mock_repository, mock_db_session):
    mock_products = [
        Product(id="MLB1", title="Test 1", price=10.0, category_id="CAT1", currency_id="BRL", available_quantity=10, thumbnail="", condition="new"),
        Product(id="MLB2", title="Test 2", price=20.0, category_id="CAT1", currency_id="BRL", available_quantity=10, thumbnail="", condition="new")
    ]
    mock_repository.get_all = AsyncMock(return_value=mock_products)
    service = ProductService(repository=mock_repository)
    
    result = await service.get_all_products(mock_db_session)
    
    assert result.status_code == 200
    assert len(result.data) == 2

@pytest.mark.asyncio
async def test_get_product_detail_success(mock_repository, mock_db_session):
    mock_product = Product(id="MLB1", title="Test Product", price=100.0, category_id="CAT1", currency_id="BRL", available_quantity=10, thumbnail="", condition="new")
    mock_repository.get_product_with_details = AsyncMock(return_value=mock_product)
    service = ProductService(repository=mock_repository)
    
    result = await service.get_product_detail(mock_db_session, "MLB1")
    
    assert result.status_code == 200
    assert result.data.id == "MLB1"

@pytest.mark.asyncio
async def test_get_product_detail_not_found(mock_repository, mock_db_session):
    mock_repository.get_product_with_details = AsyncMock(return_value=None)
    service = ProductService(repository=mock_repository)
    
    result = await service.get_product_detail(mock_db_session, "NONEXISTENT")
    
    assert result.status_code == 404

@pytest.mark.asyncio
async def test_delete_product(mock_repository, mock_db_session):
    mock_repository.delete_by_id = AsyncMock(return_value=True)
    service = ProductService(repository=mock_repository)
    
    result = await service.delete_product(mock_db_session, "MLB1")
    
    assert result.status_code == 200

@pytest.mark.asyncio
async def test_delete_all_products(mock_repository, mock_db_session):
    mock_repository.delete_all = AsyncMock()
    service = ProductService(repository=mock_repository)
    
    result = await service.delete_all_products(mock_db_session)
    
    assert result.status_code == 200
