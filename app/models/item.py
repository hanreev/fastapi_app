from pydantic import BaseModel


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class Item(ItemIn):
    id: int
