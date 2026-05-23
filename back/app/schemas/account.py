from datetime import datetime
from typing import Literal

from pydantic import BaseModel

AccountType = Literal["checking", "savings", "cash", "pix", "investment", "other"]


class AccountBase(BaseModel):
    name: str
    type: AccountType
    currency: str = "BRL"
    color: str | None = None
    icon: str | None = None


class AccountCreate(AccountBase):
    balance: float = 0.0


class AccountUpdate(BaseModel):
    name: str | None = None
    type: AccountType | None = None
    color: str | None = None
    icon: str | None = None


class AccountResponse(AccountBase):
    id: str
    user_id: str
    balance: float
    created_at: datetime

    model_config = {"from_attributes": True}