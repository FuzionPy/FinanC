from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.income import router as income_router
from app.api.v1.endpoints.expenses import router as expense_router
from app.api.v1.endpoints.reports import router as reports_router
from app.api.v1.endpoints.other_endpoints import (
    accounts_router,
    categories_router,
    goals_router,
    notifications_router,
)

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(income_router)
api_router.include_router(expense_router)
api_router.include_router(reports_router)
api_router.include_router(accounts_router)
api_router.include_router(categories_router)
api_router.include_router(goals_router)
api_router.include_router(notifications_router)