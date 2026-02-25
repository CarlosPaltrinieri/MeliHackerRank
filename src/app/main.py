from fastapi import FastAPI
from app.core.database import engine, Base, SessionLocal
from app.controllers import product_controller
from app.domain.models import Category, Product, ProductDescription
from app.core.middleware.trace_middleware import TraceMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meli Product Detail & Model API")

# Add Middlewares
app.add_middleware(TraceMiddleware)

# Seed data function
def seed_data():
    db = SessionLocal()
    # Check if data already exists
    if db.query(Category).first():
        db.close()
        return

    # Add Category
    category = Category(id="MLB1051", name="Cellphones and Smartphones")
    db.add(category)
    
    # Add Product
    product = Product(
        id="MLB123456",
        title="Samsung Galaxy S23 Ultra 512GB",
        price=5499.00,
        currency_id="BRL",
        available_quantity=10,
        thumbnail="http://http2.mlstatic.com/D_893123-MLB123456_O.jpg",
        condition="new",
        category_id="MLB1051"
    )
    db.add(product)
    
    # Add Description
    description = ProductDescription(
        product_id="MLB123456",
        text="The Galaxy S23 Ultra is Samsung's ultimate smartphone, featuring a 200MP camera and Snapdragon 8 Gen 2 processor."
    )
    db.add(description)
    
    db.commit()
    db.close()

# Run seed on startup
seed_data()

# Include Routers
app.include_router(product_controller.router)

@app.get("/health")
async def health_check():
    return {"status": "UP", "message": "Meli API is running"}
