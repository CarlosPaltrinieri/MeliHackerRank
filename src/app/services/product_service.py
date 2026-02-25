import logging
from typing import List
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.core.response import ResponseExtension
from app.domain.schemas import ProductSchema, ProductCreateSchema

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, db: Session, product_data: ProductCreateSchema) -> ResponseExtension:
        try:
            existing_product = await self.repository.get_product_with_details(db, product_data.id)
            if existing_product:
                return ResponseExtension.response(
                    status_code=400,
                    message=f"Product with ID {product_data.id} already exists."
                )
            
            created_product = await self.repository.create(db, product_data)
            
            return ResponseExtension.response(
                status_code=201,
                data=ProductSchema.model_validate(created_product),
                message="Product created successfully."
            )
        except Exception as ex:
            logger.error(f"Error in ProductService - create_product: {str(ex)}")
            return ResponseExtension.response(
                status_code=500,
                message="An internal error occurred while creating the product."
            )

    async def get_all_products(self, db: Session) -> ResponseExtension:
        try:
            products = await self.repository.get_all(db)
            data = [ProductSchema.model_validate(i) for i in products]
            return ResponseExtension.response(status_code=200, data=data)
        except Exception as ex:
            logger.error(f"Error in ProductService - get_all_products: {str(ex)}")
            return ResponseExtension.response(status_code=500, message="An internal error occurred.")

    async def get_product_detail(self, db: Session, product_id: str) -> ResponseExtension:
        try:
            product = await self.repository.get_product_with_details(db, product_id)
            
            if not product:
                return ResponseExtension.response(
                    status_code=404,
                    message=f"Product with ID {product_id} not found."
                )
            
            product_data = ProductSchema.model_validate(product)
            
            return ResponseExtension.response(
                status_code=200,
                data=product_data,
                message="Product retrieved successfully."
            )
        except Exception as ex:
            logger.error(f"Error in ProductService - get_product_detail: {str(ex)}")
            return ResponseExtension.response(
                status_code=500,
                message="An internal error occurred while retrieving the product."
            )

    async def delete_all_products(self, db: Session) -> ResponseExtension:
        try:
            await self.repository.delete_all(db)
            return ResponseExtension.response(status_code=200, message="All products deleted.")
        except Exception as ex:
            logger.error(f"Error in ProductService - delete_all_products: {str(ex)}")
            return ResponseExtension.response(status_code=500, message="An internal error occurred.")

    async def delete_product(self, db: Session, product_id: str) -> ResponseExtension:
        try:
            deleted = await self.repository.delete_by_id(db, product_id)
            if not deleted:
                return ResponseExtension.response(status_code=404, message="Product not found.")
            return ResponseExtension.response(status_code=200, message="Product deleted successfully.")
        except Exception as ex:
            logger.error(f"Error in ProductService - delete_product: {str(ex)}")
            return ResponseExtension.response(status_code=500, message="An internal error occurred.")
