from pydantic import BaseModel


class RecommendationBase(BaseModel):
    item_id: int
    recommended_item_id: int
    reason: str | None = None


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationUpdate(BaseModel):
    reason: str | None = None


class RecommendationOut(RecommendationBase):
    id: int

    class Config:
        from_attributes = True



