from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Despesas"])


@router.get("", response_model=PaginatedResponse[ExpenseResponse])
async def list_expenses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    category_id: str | None = Query(None),
    account_id: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lista despesas do usuário com filtros e paginação."""
    service = ExpenseService(db)
    return await service.list(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/pending", response_model=list[ExpenseResponse])
async def list_pending(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lista as próximas despesas pendentes (útil para o dashboard)."""
    service = ExpenseService(db)
    return await service.get_pending(current_user.id)


@router.post("", response_model=ExpenseResponse, status_code=201)
async def create_expense(
    data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ExpenseService(db)
    return await service.create(current_user.id, data)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ExpenseService(db)
    return await service.get(current_user.id, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    data: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ExpenseService(db)
    return await service.update(current_user.id, expense_id, data)


@router.delete("/{expense_id}", response_model=MessageResponse)
async def delete_expense(
    expense_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = ExpenseService(db)
    await service.delete(current_user.id, expense_id)
    return MessageResponse(message="Despesa removida com sucesso.")