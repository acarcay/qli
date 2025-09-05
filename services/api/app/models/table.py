from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Table(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branch.id", ondelete="CASCADE"), index=True, nullable=False
    )

    branch = relationship("Branch", back_populates="tables")
    orders = relationship("Order", back_populates="table")



