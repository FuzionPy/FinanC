from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, field_validator

ExpenseStatus = Literal["pending", "paid", "overdue"]
RecurrenceRule = Literal["monthly", "weekly", "yearly"]


class ExpenseBase(BaseModel):
    description: str
    amount: float
    due_date: date
    status: ExpenseStatus = "pending"
    supplier: str | None = None
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


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    due_date: date | None = None
    paid_date: date | None = None
    status: ExpenseStatus | None = None
    supplier: str | None = None
    notes: str | None = None
    is_recurring: bool | None = None
    recurrence_rule: RecurrenceRule | None = None
    category_id: str | None = None
    account_id: str | None = None


class ExpenseResponse(ExpenseBase):
    id: str
    user_id: str
    paid_date: date | None
    created_at: datetime

    model_config = {"from_attributes": True}