from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(100), unique=True, nullable=False)
    product_name = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(String(100), primary_key=True)
    stock = Column(Integer, nullable=False)
    min_stock = Column(Integer, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    ordered_at = Column(DateTime, server_default=func.now())
