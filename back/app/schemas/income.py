from datetime import datetime
from typing import Literal

from pydantic import BaseModel

CategoryType = Literal["income", "expense"]


class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    icon: str | None = None
    color: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None


class CategoryResponse(CategoryBase):
    id: str
    user_id: str
    created_at: datetime

    model_config = {"from_attributes": True}