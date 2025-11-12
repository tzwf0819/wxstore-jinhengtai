from pydantic import BaseModel

class BannerBase(BaseModel):
    image_url: str
    link_url: str | None = None
    is_active: bool = True
    sort_order: int = 0

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    image_url: str | None = None
    link_url: str | None = None
    is_active: bool | None = None
    sort_order: int | None = None

class BannerRead(BannerBase):
    id: int

    class Config:
        from_attributes = True
