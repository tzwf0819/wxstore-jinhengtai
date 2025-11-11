from pydantic import BaseModel, computed_field


class CategoryRead(BaseModel):
    id: int
    name: str
    code: str
    icon_url: str | None
    sort_order: int

    @computed_field
    @property
    def icon(self) -> str | None:
        return self.icon_url

    class Config:
        from_attributes = True
