from fastapi import FastAPI
from app.core.db import engine, Base
from app.api.endpoints import products, stocks, orders, categories, banners

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jinhengtai Mall API")

API_V1_PREFIX = "/api/v1"

app.include_router(products.router, prefix=f"{API_V1_PREFIX}/products", tags=["products"])
app.include_router(stocks.router, prefix=f"{API_V1_PREFIX}/stocks", tags=["stocks"])
app.include_router(orders.router, prefix=f"{API_V1_PREFIX}/orders", tags=["orders"])
app.include_router(categories.router, prefix=f"{API_V1_PREFIX}/categories", tags=["categories"])
app.include_router(banners.router, prefix=f"{API_V1_PREFIX}/banners", tags=["banners"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Jinhengtai Mall API"}
