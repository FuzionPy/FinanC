from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.expense import Expense
from app.repositories.base_repository import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Expense, db)

    async def get_by_user(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
        status: str | None = None,
        category_id: str | None = None,
        account_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[list[Expense], int]:
        filters = [Expense.user_id == user_id]

        if status:
            filters.append(Expense.status == status)
        if category_id:
            filters.append(Expense.category_id == category_id)
        if account_id:
            filters.append(Expense.account_id == account_id)
        if start_date:
            filters.append(Expense.due_date >= start_date)
        if end_date:
            filters.append(Expense.due_date <= end_date)

        return await self.get_all(
            filters=filters,
            offset=offset,
            limit=limit,
            order_by=Expense.due_date.desc(),
        )

    async def get_total_by_period(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
        status: str | None = None,
    ) -> float:
        filters = [
            Expense.user_id == user_id,
            Expense.due_date >= start_date,
            Expense.due_date <= end_date,
        ]
        if status:
            filters.append(Expense.status == status)

        result = await self.db.execute(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(*filters)
        )
        return float(result.scalar_one())

    async def get_pending_by_user(
        self, user_id: str, limit: int = 10
    ) -> list[Expense]:
        result = await self.db.execute(
            select(Expense)
            .where(Expense.user_id == user_id, Expense.status == "pending")
            .order_by(Expense.due_date.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_total_by_category(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> list[tuple[str | None, float]]:
        result = await self.db.execute(
            select(Expense.category_id, func.sum(Expense.amount))
            .where(
                Expense.user_id == user_id,
                Expense.due_date >= start_date,
                Expense.due_date <= end_date,
            )
            .group_by(Expense.category_id)
        )
        return result.all()