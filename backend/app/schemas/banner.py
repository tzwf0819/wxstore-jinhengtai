from pydantic import BaseModel

class BannerBase(BaseModel):
    image_url: str
    link_url: str | None = None
    is_active: bool = True
    sort_order: int = 0

class BannerRead(BannerBase):
    id: int

    class Config:
        from_attributes = True
