from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()

def import_models() -> None:
    """Import all SQLAlchemy models for metadata registration."""
    from app import models  # noqa: F401


