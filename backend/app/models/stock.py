import enum
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class StockMovementType(enum.Enum):
    INITIAL = "initial"           # 期初库存
    SALE = "sale"                 # 销售出库
    SALE_RETURN = "sale_return"     # 销售退货
    STOCK_IN = "stock_in"           # 采购入库
    STOCK_OUT_RETURN = "stock_out_return" # 采购退货

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False) # 正数表示入库，负数表示出库
    movement_type = Column(String(50), nullable=False)
    reference_id = Column(String(255), nullable=True) # 关联的订单ID、入库单ID等
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product")
