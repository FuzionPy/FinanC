from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.services.income_service import IncomeService

router = APIRouter(prefix="/incomes", tags=["Receitas"])


@router.get("", response_model=PaginatedResponse[IncomeResponse])
async def list_incomes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: str | None = Query(None),
    account_id: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lista receitas do usuário com filtros e paginação."""
    service = IncomeService(db)
    return await service.list(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        category_id=category_id,
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.post("", response_model=IncomeResponse, status_code=201)
async def create_income(
    data: IncomeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cadastra uma nova receita."""
    service = IncomeService(db)
    return await service.create(current_user.id, data)


@router.get("/{income_id}", response_model=IncomeResponse)
async def get_income(
    income_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IncomeService(db)
    return await service.get(current_user.id, income_id)


@router.patch("/{income_id}", response_model=IncomeResponse)
async def update_income(
    income_id: str,
    data: IncomeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IncomeService(db)
    return await service.update(current_user.id, income_id, data)


@router.delete("/{income_id}", response_model=MessageResponse)
async def delete_income(
    income_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = IncomeService(db)
    await service.delete(current_user.id, income_id)
    return MessageResponse(message="Receita removida com sucesso.")