import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)   # pix | transfer | cash | card
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)          # cliente/origem
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Recorrência
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_rule: Mapped[str | None] = mapped_column(String(50), nullable=True)  # monthly | weekly | yearly

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # ── Relacionamentos ───────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(back_populates="incomes")
    account: Mapped["Account"] = relationship(back_populates="incomes")
    category: Mapped["Category"] = relationship(back_populates="incomes")

    def __repr__(self) -> str:
        return f"<Income {self.description} R${self.amount}>"