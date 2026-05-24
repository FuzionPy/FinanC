from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.income import Income
from app.repositories.base_repository import BaseRepository


class IncomeRepository(BaseRepository[Income]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Income, db)

    async def get_by_user(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
        category_id: str | None = None,
        account_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[list[Income], int]:
        filters = [Income.user_id == user_id]

        if category_id:
            filters.append(Income.category_id == category_id)
        if account_id:
            filters.append(Income.account_id == account_id)
        if start_date:
            filters.append(Income.date >= start_date)
        if end_date:
            filters.append(Income.date <= end_date)

        return await self.get_all(
            filters=filters,
            offset=offset,
            limit=limit,
            order_by=Income.date.desc(),
        )

    async def get_total_by_period(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> float:
        result = await self.db.execute(
            select(func.coalesce(func.sum(Income.amount), 0)).where(
                Income.user_id == user_id,
                Income.date >= start_date,
                Income.date <= end_date,
            )
        )
        return float(result.scalar_one())

    async def get_total_by_category(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> list[tuple[str | None, float]]:
        """Retorna [(category_id, total), ...] agrupado por categoria."""
        result = await self.db.execute(
            select(Income.category_id, func.sum(Income.amount))
            .where(
                Income.user_id == user_id,
                Income.date >= start_date,
                Income.date <= end_date,
            )
            .group_by(Income.category_id)
        )
        return result.all()