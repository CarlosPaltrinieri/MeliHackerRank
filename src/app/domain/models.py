from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency_id = Column(String, default="BRL")
    available_quantity = Column(Integer, default=0)
    thumbnail = Column(String)
    condition = Column(String)
    category_id = Column(String, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    description = relationship("ProductDescription", back_populates="product", uselist=False)

class ProductDescription(Base):
    __tablename__ = "product_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    text = Column(Text)

    product = relationship("Product", back_populates="description")
