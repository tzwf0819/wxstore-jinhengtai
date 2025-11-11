from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ... import models, schemas
from ...api import deps

router = APIRouter()

@router.get("/", response_model=list[schemas.BannerRead])
def list_banners(db: Session = Depends(deps.get_db)):
    return db.query(models.Banner).order_by(models.Banner.sort_order.asc()).all()

@router.post("/", response_model=schemas.BannerRead, status_code=201)
def create_banner(banner: schemas.BannerCreate, db: Session = Depends(deps.get_db)):
    db_banner = models.Banner(**banner.model_dump())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner

@router.get("/{banner_id}", response_model=schemas.BannerRead)
def read_banner(banner_id: int, db: Session = Depends(deps.get_db)):
    db_banner = db.get(models.Banner, banner_id)
    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return db_banner

@router.put("/{banner_id}", response_model=schemas.BannerRead)
def update_banner(banner_id: int, banner: schemas.BannerCreate, db: Session = Depends(deps.get_db)):
    db_banner = db.get(models.Banner, banner_id)
    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    for key, value in banner.model_dump(exclude_unset=True).items():
        setattr(db_banner, key, value)
        
    db.commit()
    db.refresh(db_banner)
    return db_banner

@router.delete("/{banner_id}", status_code=204)
def delete_banner(banner_id: int, db: Session = Depends(deps.get_db)):
    db_banner = db.get(models.Banner, banner_id)
    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    db.delete(db_banner)
    db.commit()
