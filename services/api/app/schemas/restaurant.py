from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    slug: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class RestaurantOut(RestaurantBase):
    id: int

    class Config:
        from_attributes = True



