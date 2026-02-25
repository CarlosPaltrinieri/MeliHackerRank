import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domain.models import Base, Product, Category, ProductDescription
from app.repositories.product_repository import ProductRepository
from app.domain.schemas import ProductCreateSchema

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Pre-seed category
        cat = Category(id="CAT1", name="Test Category")
        db.add(cat)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def repository():
    return ProductRepository()

@pytest.mark.asyncio
async def test_create_product(db_session, repository):
    schema = ProductCreateSchema(
        id="MLB1",
        title="Test Product",
        price=100.0,
        category_id="CAT1",
        description_text="Test description"
    )
    created = await repository.create(db_session, schema)
    
    assert created.id == "MLB1"
    assert created.title == "Test Product"
    assert created.description.text == "Test description"

@pytest.mark.asyncio
async def test_get_all_products(db_session, repository):
    schema1 = ProductCreateSchema(id="MLB1", title="Test Product 1", price=100.0, category_id="CAT1")
    schema2 = ProductCreateSchema(id="MLB2", title="Test Product 2", price=200.0, category_id="CAT1")
    await repository.create(db_session, schema1)
    await repository.create(db_session, schema2)
    
    products = await repository.get_all(db_session)
    assert len(products) == 2

@pytest.mark.asyncio
async def test_get_product_with_details(db_session, repository):
    schema = ProductCreateSchema(id="MLB1", title="Test Product", price=100.0, category_id="CAT1")
    await repository.create(db_session, schema)
    
    product = await repository.get_product_with_details(db_session, "MLB1")
    assert product is not None
    assert product.title == "Test Product"

@pytest.mark.asyncio
async def test_delete_by_id(db_session, repository):
    schema = ProductCreateSchema(id="MLB1", title="Test Product", price=100.0, category_id="CAT1")
    await repository.create(db_session, schema)
    
    deleted = await repository.delete_by_id(db_session, "MLB1")
    assert deleted is True
    
    product = await repository.get_product_with_details(db_session, "MLB1")
    assert product is None

@pytest.mark.asyncio
async def test_delete_all(db_session, repository):
    schema = ProductCreateSchema(id="MLB1", title="Test Product", price=100.0, category_id="CAT1")
    await repository.create(db_session, schema)
    
    await repository.delete_all(db_session)
    
    products = await repository.get_all(db_session)
    assert len(products) == 0
