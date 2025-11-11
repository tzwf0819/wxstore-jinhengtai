from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.banner import Banner
from ...schemas.banner import BannerRead

router = APIRouter(prefix="/banners", tags=["banners"])


@router.get("/", response_model=list[BannerRead])
def list_banners(db: Session = Depends(get_db)) -> list[BannerRead]:
    banners: Sequence[Banner] = db.scalars(
        select(Banner).where(Banner.is_active.is_(True)).order_by(Banner.sort_order.asc())
    ).all()

    return [BannerRead.model_validate(banner) for banner in banners]
