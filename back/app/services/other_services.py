from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.repositories.other_repositories import (
    AccountRepository,
    CategoryRepository,
    GoalRepository,
    NotificationRepository,
)
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.schemas.notification import NotificationResponse


# ── Account Service ───────────────────────────────────────────────────────────

class AccountService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = AccountRepository(db)

    async def list(self, user_id: str) -> list[AccountResponse]:
        items = await self.repo.get_by_user(user_id)
        return [AccountResponse.model_validate(i) for i in items]

    async def create(self, user_id: str, data: AccountCreate) -> AccountResponse:
        account = await self.repo.create({**data.model_dump(), "user_id": user_id})
        return AccountResponse.model_validate(account)

    async def update(self, user_id: str, account_id: str, data: AccountUpdate) -> AccountResponse:
        account = await self.repo.get_by_id(account_id)
        if not account:
            raise NotFoundException("Conta")
        if account.user_id != user_id:
            raise ForbiddenException()
        updated = await self.repo.update(account, data.model_dump(exclude_none=True))
        return AccountResponse.model_validate(updated)

    async def delete(self, user_id: str, account_id: str) -> None:
        account = await self.repo.get_by_id(account_id)
        if not account:
            raise NotFoundException("Conta")
        if account.user_id != user_id:
            raise ForbiddenException()
        await self.repo.delete(account)


# ── Category Service ──────────────────────────────────────────────────────────

class CategoryService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = CategoryRepository(db)

    async def list(self, user_id: str, type: str | None = None) -> list[CategoryResponse]:
        items = await self.repo.get_by_user(user_id, type=type)
        return [CategoryResponse.model_validate(i) for i in items]

    async def create(self, user_id: str, data: CategoryCreate) -> CategoryResponse:
        category = await self.repo.create({**data.model_dump(), "user_id": user_id})
        return CategoryResponse.model_validate(category)

    async def update(self, user_id: str, category_id: str, data: CategoryUpdate) -> CategoryResponse:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Categoria")
        if category.user_id != user_id:
            raise ForbiddenException()
        updated = await self.repo.update(category, data.model_dump(exclude_none=True))
        return CategoryResponse.model_validate(updated)

    async def delete(self, user_id: str, category_id: str) -> None:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Categoria")
        if category.user_id != user_id:
            raise ForbiddenException()
        await self.repo.delete(category)


# ── Goal Service ──────────────────────────────────────────────────────────────

class GoalService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = GoalRepository(db)

    async def list(self, user_id: str, status: str | None = None) -> list[GoalResponse]:
        items = await self.repo.get_by_user(user_id, status=status)
        return [GoalResponse.model_validate(i) for i in items]

    async def create(self, user_id: str, data: GoalCreate) -> GoalResponse:
        goal = await self.repo.create({**data.model_dump(), "user_id": user_id})
        return GoalResponse.model_validate(goal)

    async def update(self, user_id: str, goal_id: str, data: GoalUpdate) -> GoalResponse:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise NotFoundException("Meta")
        if goal.user_id != user_id:
            raise ForbiddenException()
        updated = await self.repo.update(goal, data.model_dump(exclude_none=True))
        return GoalResponse.model_validate(updated)

    async def delete(self, user_id: str, goal_id: str) -> None:
        goal = await self.repo.get_by_id(goal_id)
        if not goal:
            raise NotFoundException("Meta")
        if goal.user_id != user_id:
            raise ForbiddenException()
        await self.repo.delete(goal)


# ── Notification Service ──────────────────────────────────────────────────────

class NotificationService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = NotificationRepository(db)

    async def list(self, user_id: str, unread_only: bool = False) -> list[NotificationResponse]:
        items = await self.repo.get_by_user(user_id, unread_only=unread_only)
        return [NotificationResponse.model_validate(i) for i in items]

    async def mark_read(self, user_id: str, ids: list[str]) -> None:
        await self.repo.mark_as_read(user_id, ids)