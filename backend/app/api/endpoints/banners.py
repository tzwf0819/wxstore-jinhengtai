
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.banner import Banner
from app.schemas.banner import Banner as BannerSchema

router = APIRouter()


@router.get("/", response_model=List[BannerSchema])
def read_banners(
    db: Session = Depends(deps.get_db),
):
    """
    Retrieve banners.
    """
    banners = db.query(Banner).all()
    return banners
