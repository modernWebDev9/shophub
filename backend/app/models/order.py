from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), default="pending")
    subtotal = Column(Float, nullable=False)
    shipping_cost = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    shipping_first_name = Column(String(100), nullable=False)
    shipping_last_name = Column(String(100), nullable=False)
    shipping_address_line1 = Column(String(255), nullable=False)
    shipping_address_line2 = Column(String(255))
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100), nullable=False)
    shipping_postal_code = Column(String(20), nullable=False)
    shipping_country = Column(String(100), default="India")
    shipping_phone = Column(String(20))
    shipping_method = Column(String(50), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(50), default="pending")
    tracking_number = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String(255), nullable=False)
    product_sku = Column(String(100))
    product_image = Column(String(500))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    variant_attributes = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())