from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, ARRAY, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    short_description = Column(String(500))
    description = Column(Text)
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float)
    sku = Column(String(100), unique=True)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand = Column(String(100))
    tags = Column(ARRAY(String))
    views_count = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())