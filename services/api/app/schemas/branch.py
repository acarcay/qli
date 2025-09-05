from pydantic import BaseModel


class BranchBase(BaseModel):
    name: str
    restaurant_id: int


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: str | None = None


class BranchOut(BranchBase):
    id: int

    class Config:
        from_attributes = True



