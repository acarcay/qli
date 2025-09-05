from sqlalchemy import Integer, String, ForeignKey, Enum, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.db.base import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    preparing = "preparing"
    served = "served"
    cancelled = "cancelled"


class Order(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branch.id", ondelete="CASCADE"), index=True)
    table_id: Mapped[int | None] = mapped_column(ForeignKey("table.id", ondelete="SET NULL"), index=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), index=True, default=OrderStatus.pending)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    branch = relationship("Branch", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


Index("ix_orders_branch_status_created_at", Order.branch_id, Order.status, Order.created_at)


class OrderItem(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    item = relationship("Item", back_populates="order_items")



