from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.income import Income
from app.repositories.income_repository import IncomeRepository
from app.schemas.common import PaginatedResponse
from app.schemas.income import IncomeCreate, IncomeResponse, IncomeUpdate


class IncomeService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = IncomeRepository(db)

    async def list(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        category_id: str | None = None,
        account_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> PaginatedResponse[IncomeResponse]:
        offset = (page - 1) * page_size
        items, total = await self.repo.get_by_user(
            user_id=user_id,
            offset=offset,
            limit=page_size,
            category_id=category_id,
            account_id=account_id,
            start_date=start_date,
            end_date=end_date,
        )
        return PaginatedResponse.build(
            items=[IncomeResponse.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def create(self, user_id: str, data: IncomeCreate) -> IncomeResponse:
        income = await self.repo.create({
            **data.model_dump(),
            "user_id": user_id,
        })
        return IncomeResponse.model_validate(income)

    async def get(self, user_id: str, income_id: str) -> IncomeResponse:
        income = await self._get_owned(user_id, income_id)
        return IncomeResponse.model_validate(income)

    async def update(
        self, user_id: str, income_id: str, data: IncomeUpdate
    ) -> IncomeResponse:
        income = await self._get_owned(user_id, income_id)
        updated = await self.repo.update(
            income, data.model_dump(exclude_none=True)
        )
        return IncomeResponse.model_validate(updated)

    async def delete(self, user_id: str, income_id: str) -> None:
        income = await self._get_owned(user_id, income_id)
        await self.repo.delete(income)

    async def _get_owned(self, user_id: str, income_id: str) -> Income:
        income = await self.repo.get_by_id(income_id)
        if not income:
            raise NotFoundException("Receita")
        if income.user_id != user_id:
            raise ForbiddenException()
        return income