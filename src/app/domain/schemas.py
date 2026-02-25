from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str

class ProductDescriptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str

class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    price: float
    currency_id: str
    available_quantity: int
    thumbnail: str
    condition: str
    category_id: str
    category: Optional[CategorySchema] = None
    description: Optional[ProductDescriptionSchema] = None

class ProductCreateSchema(BaseModel):
    id: str
    title: str
    price: float
    currency_id: str = "BRL"
    available_quantity: int = 0
    thumbnail: str = ""
    condition: str = "new"
    category_id: str
    description_text: Optional[str] = None

