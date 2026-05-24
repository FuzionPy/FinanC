from datetime import date

from pydantic import BaseModel


class ReportParams(BaseModel):
    start_date: date
    end_date: date
    account_id: str | None = None
    category_id: str | None = None


class CashFlowItem(BaseModel):
    month: str          # "2025-01"
    income: float
    expense: float
    balance: float


class CategorySummary(BaseModel):
    category_id: str | None
    category_name: str
    total: float
    percentage: float


class MonthlySummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    income_by_category: list[CategorySummary]
    expense_by_category: list[CategorySummary]
    cash_flow: list[CashFlowItem]