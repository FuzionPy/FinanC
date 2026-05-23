import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    current_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | achieved | cancelled
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # ── Relacionamentos ───────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(back_populates="goals")
    category: Mapped["Category"] = relationship(back_populates="goals")

    @property
    def progress_percent(self) -> float:
        """Percentual de progresso da meta (0-100)."""
        if self.target_amount == 0:
            return 0.0
        return min(round((self.current_amount / self.target_amount) * 100, 2), 100.0)

    def __repr__(self) -> str:
        return f"<Goal {self.title} {self.progress_percent}%>"