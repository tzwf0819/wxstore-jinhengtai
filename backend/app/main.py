from fastapi import FastAPI
from app.core.db import engine, Base
from app.api.endpoints import products, stocks, orders

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mall API"}
