from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.category import Category
from app.models.goal import Goal
from app.models.notification import Notification
from app.repositories.base_repository import BaseRepository


# ── Account ───────────────────────────────────────────────────────────────────

class AccountRepository(BaseRepository[Account]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Account, db)

    async def get_by_user(self, user_id: str) -> list[Account]:
        result = await self.db.execute(
            select(Account)
            .where(Account.user_id == user_id)
            .order_by(Account.name.asc())
        )
        return list(result.scalars().all())


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryRepository(BaseRepository[Category]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Category, db)

    async def get_by_user(
        self, user_id: str, type: str | None = None
    ) -> list[Category]:
        query = select(Category).where(Category.user_id == user_id)
        if type:
            query = query.where(Category.type == type)
        query = query.order_by(Category.name.asc())
        result = await self.db.execute(query)
        return list(result.scalars().all())


# ── Goal ──────────────────────────────────────────────────────────────────────

class GoalRepository(BaseRepository[Goal]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Goal, db)

    async def get_by_user(
        self, user_id: str, status: str | None = None
    ) -> list[Goal]:
        query = select(Goal).where(Goal.user_id == user_id)
        if status:
            query = query.where(Goal.status == status)
        query = query.order_by(Goal.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())


# ── Notification ──────────────────────────────────────────────────────────────

class NotificationRepository(BaseRepository[Notification]):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Notification, db)

    async def get_by_user(
        self, user_id: str, unread_only: bool = False
    ) -> list[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read == False)  # noqa: E712
        query = query.order_by(Notification.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def mark_as_read(self, user_id: str, ids: list[str]) -> None:
        from sqlalchemy import update
        await self.db.execute(
            update(Notification)
            .where(Notification.user_id == user_id, Notification.id.in_(ids))
            .values(is_read=True)
        )
        await self.db.flush()