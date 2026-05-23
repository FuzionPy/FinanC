from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


# ── Paginação ─────────────────────────────────────────────────────────────────

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int, page_size: int) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=-(-total // page_size),  # ceil division
        )


# ── Resposta padrão ───────────────────────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str