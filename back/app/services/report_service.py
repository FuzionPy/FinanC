from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.expense_repository import ExpenseRepository
from app.repositories.income_repository import IncomeRepository
from app.repositories.other_repositories import CategoryRepository
from app.schemas.report import CategorySummary, MonthlySummary


class ReportService:

    def __init__(self, db: AsyncSession) -> None:
        self.income_repo = IncomeRepository(db)
        self.expense_repo = ExpenseRepository(db)
        self.category_repo = CategoryRepository(db)

    async def monthly_summary(
        self,
        user_id: str,
        start_date: date,
        end_date: date,
    ) -> MonthlySummary:
        # Totais gerais
        total_income = await self.income_repo.get_total_by_period(user_id, start_date, end_date)
        total_expense = await self.expense_repo.get_total_by_period(user_id, start_date, end_date)

        # Por categoria — receitas
        income_by_cat_raw = await self.income_repo.get_total_by_category(user_id, start_date, end_date)
        income_by_category = await self._build_category_summary(
            user_id, income_by_cat_raw, total_income, "income"
        )

        # Por categoria — despesas
        expense_by_cat_raw = await self.expense_repo.get_total_by_category(user_id, start_date, end_date)
        expense_by_category = await self._build_category_summary(
            user_id, expense_by_cat_raw, total_expense, "expense"
        )

        return MonthlySummary(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense,
            income_by_category=income_by_category,
            expense_by_category=expense_by_category,
            cash_flow=[],  # implementado na próxima iteração
        )

    async def _build_category_summary(
        self,
        user_id: str,
        raw: list[tuple],
        total: float,
        type: str,
    ) -> list[CategorySummary]:
        categories = await self.category_repo.get_by_user(user_id, type=type)
        cat_map = {c.id: c.name for c in categories}

        result = []
        for category_id, amount in raw:
            result.append(CategorySummary(
                category_id=category_id,
                category_name=cat_map.get(category_id, "Sem categoria"),
                total=float(amount),
                percentage=round((float(amount) / total * 100), 2) if total > 0 else 0.0,
            ))

        return sorted(result, key=lambda x: x.total, reverse=True)