from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ...core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/ping")
def ping(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
