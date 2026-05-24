from __future__ import annotations

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.common import PaginatedResponse
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate


class ExpenseService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = ExpenseRepository(db)

    async def list(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        category_id: str | None = None,
        account_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> PaginatedResponse[ExpenseResponse]:
        offset = (page - 1) * page_size
        items, total = await self.repo.get_by_user(
            user_id=user_id,
            offset=offset,
            limit=page_size,
            status=status,
            category_id=category_id,
            account_id=account_id,
            start_date=start_date,
            end_date=end_date,
        )
        return PaginatedResponse.build(
            items=[ExpenseResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def create(self, user_id: str, data: ExpenseCreate) -> ExpenseResponse:
        expense = await self.repo.create({
            **data.model_dump(),
            "user_id": user_id,
        })
        return ExpenseResponse.model_validate(expense)

    async def get(self, user_id: str, expense_id: str) -> ExpenseResponse:
        expense = await self._get_owned(user_id, expense_id)
        return ExpenseResponse.model_validate(expense)

    async def update(
        self, user_id: str, expense_id: str, data: ExpenseUpdate
    ) -> ExpenseResponse:
        expense = await self._get_owned(user_id, expense_id)
        updated = await self.repo.update(
            expense, data.model_dump(exclude_none=True)
        )
        return ExpenseResponse.model_validate(updated)

    async def delete(self, user_id: str, expense_id: str) -> None:
        expense = await self._get_owned(user_id, expense_id)
        await self.repo.delete(expense)

    async def get_pending(self, user_id: str) -> list[ExpenseResponse]:
        items = await self.repo.get_pending_by_user(user_id)
        return [ExpenseResponse.model_validate(i) for i in items]

    async def _get_owned(self, user_id: str, expense_id: str) -> Expense:
        expense = await self.repo.get_by_id(expense_id)
        if not expense:
            raise NotFoundException("Despesa")
        if expense.user_id != user_id:
            raise ForbiddenException()
        return expense