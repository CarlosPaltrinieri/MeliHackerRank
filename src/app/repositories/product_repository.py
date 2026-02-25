from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models import Product, ProductDescription
from app.domain.schemas import ProductCreateSchema

class ProductRepository:
    def __init__(self):
        pass

    async def get_all(self, db: Session) -> List[Product]:
        return db.query(Product).all()
    
    async def get_product_with_details(self, db: Session, product_id: str) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()
        
    async def create(self, db: Session, product_data: ProductCreateSchema) -> Product:
        new_product = Product(
            id=product_data.id,
            title=product_data.title,
            price=product_data.price,
            currency_id=product_data.currency_id,
            available_quantity=product_data.available_quantity,
            thumbnail=product_data.thumbnail,
            condition=product_data.condition,
            category_id=product_data.category_id
        )
        db.add(new_product)
        
        if product_data.description_text:
            description = ProductDescription(product_id=new_product.id, text=product_data.description_text)
            db.add(description)
            
        db.commit()
        db.refresh(new_product)
        return new_product
        
    async def delete_by_id(self, db: Session, product_id: str) -> bool:
        product = await self.get_product_with_details(db, product_id)
        if product:
            # SQLAlchemy will cascade delete if configured, or we delete children explicitly
            if product.description:
                db.delete(product.description)
            db.delete(product)
            db.commit()
            return True
        return False
        
    async def delete_all(self, db: Session) -> None:
        db.query(ProductDescription).delete()
        db.query(Product).delete()
        db.commit()
