from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    price: float
    short_description: Optional[str] = None
    description: Optional[str] = None
    quantity: int = 0
    category_id: Optional[int] = None
    sku: Optional[str] = None
    brand: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    category_id: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    short_description: Optional[str]
    description: Optional[str]
    price: float
    compare_at_price: Optional[float]
    sku: Optional[str]
    quantity: int
    is_active: bool
    is_featured: bool
    category_id: Optional[int]
    category_name: Optional[str] = None
    brand: Optional[str]
    tags: Optional[List[str]]
    rating_avg: float
    rating_count: int
    images: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True