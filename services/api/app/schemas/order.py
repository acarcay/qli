from pydantic import BaseModel
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    item_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    branch_id: int
    table_id: int | None = None
    status: OrderStatus | None = None


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = []


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderOut(OrderBase):
    id: int

    class Config:
        from_attributes = True



