import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # checking | savings | cash | pix
    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="BRL")
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)   # hex color
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # ── Relacionamentos ───────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(back_populates="accounts")
    incomes: Mapped[list["Income"]] = relationship(back_populates="account")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"<Account {self.name} ({self.type})>"