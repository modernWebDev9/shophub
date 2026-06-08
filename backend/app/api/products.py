from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.product import Product, ProductImage
from app.models.category import Category
from typing import Optional, List

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/")
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    sort: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_active == True)
    
    # Category filter
    if category:
        query = query.join(Category).filter(Category.slug == category)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.short_description.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%")
            )
        )
    
    # Price filter
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    # Featured filter
    if featured:
        query = query.filter(Product.is_featured == True)
    
    # Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    elif sort == "popular":
        query = query.order_by(Product.sold_count.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating_avg.desc())
    else:
        query = query.order_by(Product.id.desc())
    
    # Pagination
    total = query.count()
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()
    
    # Format response with images
    result = []
    for product in products:
        images = db.query(ProductImage.image_url).filter(
            ProductImage.product_id == product.id
        ).order_by(ProductImage.sort_order).all()
        
        category_name = None
        if product.category_id:
            cat = db.query(Category).filter(Category.id == product.category_id).first()
            category_name = cat.name if cat else None
        
        result.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "short_description": product.short_description,
            "description": product.description,
            "price": product.price,
            "compare_at_price": product.compare_at_price,
            "sku": product.sku,
            "quantity": product.quantity,
            "is_active": product.is_active,
            "is_featured": product.is_featured,
            "brand": product.brand,
            "rating_avg": product.rating_avg,
            "rating_count": product.rating_count,
            "category_id": product.category_id,
            "category_name": category_name,
            "images": [img[0] for img in images],
            "created_at": product.created_at
        })
    
    return {
        "products": result,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order).all()
    return [
        {
            "id": c.id, 
            "name": c.name, 
            "slug": c.slug, 
            "description": c.description,
            "image_url": c.image_url
        } 
        for c in categories
    ]

@router.get("/featured")
def get_featured_products(limit: int = 8, db: Session = Depends(get_db)):
    """Get featured products"""
    products = db.query(Product).filter(
        Product.is_active == True,
        Product.is_featured == True
    ).limit(limit).all()
    
    result = []
    for product in products:
        primary_image = db.query(ProductImage.image_url).filter(
            ProductImage.product_id == product.id,
            ProductImage.is_primary == True
        ).first()
        
        result.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "short_description": product.short_description,
            "price": product.price,
            "compare_at_price": product.compare_at_price,
            "quantity": product.quantity,
            "brand": product.brand,
            "rating_avg": product.rating_avg,
            "images": [primary_image[0]] if primary_image else [],
            "created_at": product.created_at
        })
    
    return result

@router.get("/{slug}")
def get_product(slug: str, db: Session = Depends(get_db)):
    """Get single product by slug"""
    product = db.query(Product).filter(Product.slug == slug, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Increment view count
    product.views_count += 1
    db.commit()
    
    # Get images
    images = db.query(ProductImage).filter(
        ProductImage.product_id == product.id
    ).order_by(ProductImage.sort_order).all()
    
    # Get category
    category = None
    if product.category_id:
        cat = db.query(Category).filter(Category.id == product.category_id).first()
        if cat:
            category = {"id": cat.id, "name": cat.name, "slug": cat.slug}
    
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "short_description": product.short_description,
        "description": product.description,
        "price": product.price,
        "compare_at_price": product.compare_at_price,
        "sku": product.sku,
        "quantity": product.quantity,
        "is_active": product.is_active,
        "is_featured": product.is_featured,
        "brand": product.brand,
        "tags": product.tags,
        "rating_avg": product.rating_avg,
        "rating_count": product.rating_count,
        "views_count": product.views_count,
        "category": category,
        "images": [{"id": img.id, "url": img.image_url, "is_primary": img.is_primary} for img in images],
        "created_at": product.created_at
    }