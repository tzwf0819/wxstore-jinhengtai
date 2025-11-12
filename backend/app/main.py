import os
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.web.admin import router as admin_web_router
from app.api.endpoints import admin as admin_api_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Jinhengtai Mall API")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Static files and Templates ---
# Get the absolute path to the directory containing main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- API Routes ---
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/jinhengtai/api/v1")
app.include_router(api_router, prefix="/api/v1/v1")
app.include_router(api_router, prefix="/api")

# --- Web Admin Routes ---
app.include_router(admin_web_router, tags=["admin-web"])
app.include_router(admin_api_router.router, prefix="/admin/api", tags=["admin-api"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jinhengtai Mall API. Visit /admin/products for the web admin."}
