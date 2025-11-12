import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi import APIRouter
from app.web.admin import router as web_router
from app.api.endpoints import banners, categories, orders, products, stock, admin as admin_api_router

# Create the FastAPI app instance
app = FastAPI(title="Jinhengtai Mall API", root_path="/jinhengtai")

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
# All API routes are prefixed with /jinhengtai for proxy compatibility
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(banners.router, prefix="/banners", tags=["Banners"])
api_router.include_router(stock.router, prefix="/stock", tags=["Stock"])

app.include_router(api_router)


# --- Web Admin Routes ---
# The /admin routes are for the web-based administrative interface.
app.include_router(web_router, tags=["Admin Web"])
# The /admin/api routes are for internal API calls from the admin interface.
app.include_router(admin_api_router.router, prefix="/admin/api", tags=["Admin API"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jinhengtai Mall API."}
