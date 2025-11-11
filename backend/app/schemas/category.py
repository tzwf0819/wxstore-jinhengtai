from pydantic import BaseModel


class CategoryRead(BaseModel):
    id: int
    name: str
    code: str
    icon_url: str | None
    sort_order: int

    class Config:
        from_attributes = True
