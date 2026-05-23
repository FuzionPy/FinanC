from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import MonthlySummary
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Relatórios"])


@router.get("/summary", response_model=MonthlySummary)
async def monthly_summary(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Resumo financeiro do período: totais, saldo e breakdown por categoria.
    Usado pelo dashboard e pela tela de relatórios.
    """
    service = ReportService(db)
    return await service.monthly_summary(current_user.id, start_date, end_date)