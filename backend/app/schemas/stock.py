from pydantic import BaseModel

class StockMovementBase(BaseModel):
    product_id: int
    quantity: int
    reference_id: str | None = None

class StockMovementCreate(StockMovementBase):
    pass

class StockMovementRead(StockMovementBase):
    id: int
    movement_type: str

    class Config:
        from_attributes = True
