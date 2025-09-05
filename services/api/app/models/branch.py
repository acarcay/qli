from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Branch(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurant.id", ondelete="CASCADE"), index=True, nullable=False
    )

    restaurant = relationship("Restaurant", back_populates="branches")
    tables = relationship(
        "Table",
        back_populates="branch",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    menus = relationship(
        "Menu",
        back_populates="branch",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    orders = relationship("Order", back_populates="branch")



