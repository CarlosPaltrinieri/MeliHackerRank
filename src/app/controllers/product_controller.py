from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.core.response import ResponseExtension
from app.domain.schemas import ProductCreateSchema
import logging

router = APIRouter(prefix="/api/products", tags=["products"])
logger = logging.getLogger(__name__)

def get_product_service():
    return ProductService(ProductRepository())

@router.post("")
async def create_product(
    product: ProductCreateSchema,
    service: ProductService = Depends(get_product_service),
    db: Session = Depends(get_db)
):
    result = await service.create_product(db, product)
    return JSONResponse(
        status_code=result.status_code, 
        content=result.model_dump()
    )

@router.get("")
async def get_all_products(
    service: ProductService = Depends(get_product_service),
    db: Session = Depends(get_db)
):
    result = await service.get_all_products(db)
    # Re-build the response extension data by dumping individual models to prevent serialization issues with 'Any'
    if result.data:
        result.data = [item.model_dump() for item in result.data]
    
    return JSONResponse(
        status_code=result.status_code, 
        content=result.model_dump()
    )

@router.get("/{product_id}")
async def get_product(
    product_id: str, 
    service: ProductService = Depends(get_product_service),
    db: Session = Depends(get_db)
):
    result = await service.get_product_detail(db, product_id)
    if result.data and hasattr(result.data, "model_dump"):
        result.data = result.data.model_dump()
        
    return JSONResponse(
        status_code=result.status_code, 
        content=result.model_dump()
    )

@router.delete("/erase")
async def delete_all_products(
    service: ProductService = Depends(get_product_service),
    db: Session = Depends(get_db)
):
    result = await service.delete_all_products(db)
    return JSONResponse(
        status_code=result.status_code, 
        content=result.model_dump()
    )

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
    db: Session = Depends(get_db)
):
    result = await service.delete_product(db, product_id)
    return JSONResponse(
        status_code=result.status_code, 
        content=result.model_dump()
    )
