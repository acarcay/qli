from sqlalchemy import Integer, String, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Menu(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branch.id", ondelete="CASCADE"), index=True, nullable=False
    )

    branch = relationship("Branch", back_populates="menus")
    categories = relationship(
        "Category",
        back_populates="menu",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menu.id", ondelete="CASCADE"), index=True, nullable=False
    )

    menu = relationship("Menu", back_populates="categories")
    items = relationship(
        "Item",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Item(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE"), index=True, nullable=False
    )

    category = relationship("Category", back_populates="items")
    options = relationship(
        "ItemOption",
        back_populates="item",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    order_items = relationship("OrderItem", back_populates="item")


class ItemOption(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_delta_cents: Mapped[int] = mapped_column(Integer, default=0)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="CASCADE"), index=True, nullable=False
    )

    item = relationship("Item", back_populates="options")


# FTS index for items (name + description)
Index(
    "ix_item_fts",
    text("to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(description,''))"),
    postgresql_using="gin",
)


