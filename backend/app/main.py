import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.web.admin import router as admin_web_router
from app.api.endpoints import admin as admin_api_router

# Create the FastAPI app instance
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_dir = os.path.join(BASE_DIR, "static")
os.makedirs(os.path.join(static_dir, "uploads"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- API Routes ---
app.include_router(api_router, prefix="/api/v1")

# --- Web Admin Routes ---
app.include_router(admin_web_router, tags=["admin-web"])
app.include_router(admin_api_router.router, prefix="/admin/api", tags=["admin-api"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jinhengtai Mall API."}
