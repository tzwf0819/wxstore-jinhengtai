
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.banner import Banner
from app.schemas.banner import BannerCreate, BannerRead, BannerUpdate

router = APIRouter()


@router.post("/", response_model=BannerRead, status_code=201)
def create_banner(
    *, db: Session = Depends(deps.get_db), banner_in: BannerCreate
):
    """
    Create a new banner.
    """
    banner = Banner(**banner_in.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner


@router.get("", response_model=List[BannerRead])
def read_banners(
    db: Session = Depends(deps.get_db),
):
    """
    Retrieve banners.
    """
    banners = db.query(Banner).all()
    return banners


@router.get("/{banner_id}", response_model=BannerRead)
def read_banner(
    *, db: Session = Depends(deps.get_db), banner_id: int
):
    """
    Get a banner by ID.
    """
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner


@router.put("/{banner_id}", response_model=BannerRead)
def update_banner(
    *, db: Session = Depends(deps.get_db), banner_id: int, banner_in: BannerUpdate
):
    """
    Update a banner.
    """
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    update_data = banner_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(banner, field, value)
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner


@router.delete("/{banner_id}", status_code=204)
def delete_banner(
    *, db: Session = Depends(deps.get_db), banner_id: int
):
    """
    Delete a banner.
    """
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    db.delete(banner)
    db.commit()
    return
