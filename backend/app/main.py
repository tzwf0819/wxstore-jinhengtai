from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.web.admin import router as admin_web_router
from app.api.endpoints import admin as admin_api_router

app = FastAPI(title="Jinhengtai Mall API", root_path="/jinhengtai")

# --- Static files and Templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- API Routes ---
API_V1_PREFIX = "/api/v1"
app.include_router(api_router, prefix=API_V1_PREFIX)

# --- Web Admin Routes ---
app.include_router(admin_web_router, tags=["admin-web"])
app.include_router(admin_api_router.router, prefix="/admin/api", tags=["admin-api"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jinhengtai Mall API. Visit /admin/products for the web admin."}
