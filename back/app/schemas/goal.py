from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, field_validator

GoalStatus = Literal["active", "achieved", "cancelled"]


class GoalBase(BaseModel):
    title: str
    description: str | None = None
    target_amount: float
    deadline: date | None = None
    icon: str | None = None
    color: str | None = None
    category_id: str | None = None

    @field_validator("target_amount")
    @classmethod
    def target_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("O valor alvo deve ser maior que zero.")
        return round(v, 2)


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_amount: float | None = None
    current_amount: float | None = None
    deadline: date | None = None
    status: GoalStatus | None = None
    icon: str | None = None
    color: str | None = None


class GoalResponse(GoalBase):
    id: str
    user_id: str
    current_amount: float
    status: GoalStatus
    progress_percent: float
    created_at: datetime

    model_config = {"from_attributes": True}