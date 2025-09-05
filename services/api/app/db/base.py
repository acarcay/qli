from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()


# Import models here so Alembic can auto-detect
from app.models import (  # noqa: F401
    User,
    Restaurant,
    Branch,
    Table,
    Menu,
    Category,
    Item,
    ItemOption,
    Order,
    OrderItem,
    Recommendation,
)


