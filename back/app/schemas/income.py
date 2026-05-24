from datetime import date as DateType, datetime
from typing import Literal

from pydantic import BaseModel, field_validator

PaymentMethod = Literal["pix", "transfer", "cash", "card", "other"]
RecurrenceRule = Literal["monthly", "weekly", "yearly"]


class IncomeBase(BaseModel):
    description: str
    amount: float
    date: DateType
    payment_method: PaymentMethod | None = None
    source: str | None = None
    notes: str | None = None
    is_recurring: bool = False
    recurrence_rule: RecurrenceRule | None = None
    category_id: str | None = None
    account_id: str | None = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return round(v, 2)


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: DateType | None = None
    payment_method: PaymentMethod | None = None
    source: str | None = None
    notes: str | None = None
    is_recurring: bool | None = None
    recurrence_rule: RecurrenceRule | None = None
    category_id: str | None = None
    account_id: str | None = None


class IncomeResponse(IncomeBase):
    id: str
    user_id: str
    created_at: datetime

    model_config = {"from_attributes": True}