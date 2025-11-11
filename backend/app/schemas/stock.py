from pydantic import BaseModel

class StockBase(BaseModel):
    product_id: int
    quantity: int

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id: int

    class Config:
        orm_mode = True
