import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)   # income | expense
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)   # hex color
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ── Relacionamentos ───────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(back_populates="categories")
    incomes: Mapped[list["Income"]] = relationship(back_populates="category")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")
    goals: Mapped[list["Goal"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.type})>"