from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repository genérico com operações CRUD reutilizáveis.
    Todos os repositories específicos herdam desta classe.

    Uso:
        class UserRepository(BaseRepository[User]):
            def __init__(self, db: AsyncSession):
                super().__init__(User, db)
    """

    def __init__(self, model: type[ModelType], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    # ── Leitura ───────────────────────────────────────────────────────────────

    async def get_by_id(self, id: str) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        filters: list[Any] | None = None,
        offset: int = 0,
        limit: int = 20,
        order_by: Any = None,
    ) -> tuple[list[ModelType], int]:
        """Retorna (items, total) com suporte a filtros e paginação."""
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        if filters:
            for f in filters:
                query = query.where(f)
                count_query = count_query.where(f)

        if order_by is not None:
            query = query.order_by(order_by)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return items, total

    # ── Escrita ───────────────────────────────────────────────────────────────

    async def create(self, data: dict[str, Any]) -> ModelType:
        instance = self.model(**data)
        self.db.add(instance)
        await self.db.flush()       # persiste sem commit (commit é feito na sessão)
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: ModelType, data: dict[str, Any]) -> ModelType:
        for field, value in data.items():
            if hasattr(instance, field) and value is not None:
                setattr(instance, field, value)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.db.delete(instance)
        await self.db.flush()

    # ── Utilitários ───────────────────────────────────────────────────────────

    async def exists(self, filters: list[Any]) -> bool:
        query = select(func.count()).select_from(self.model)
        for f in filters:
            query = query.where(f)
        result = await self.db.execute(query)
        return result.scalar_one() > 0