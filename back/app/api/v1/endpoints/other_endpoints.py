from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.common import MessageResponse
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.schemas.notification import NotificationMarkRead, NotificationResponse
from app.services.other_services import (
    AccountService,
    CategoryService,
    GoalService,
    NotificationService,
)

# ── Accounts ──────────────────────────────────────────────────────────────────
accounts_router = APIRouter(prefix="/accounts", tags=["Contas"])


@accounts_router.get("", response_model=list[AccountResponse])
async def list_accounts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await AccountService(db).list(current_user.id)


@accounts_router.post("", response_model=AccountResponse, status_code=201)
async def create_account(data: AccountCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await AccountService(db).create(current_user.id, data)


@accounts_router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: str, data: AccountUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await AccountService(db).update(current_user.id, account_id, data)


@accounts_router.delete("/{account_id}", response_model=MessageResponse)
async def delete_account(account_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await AccountService(db).delete(current_user.id, account_id)
    return MessageResponse(message="Conta removida com sucesso.")


# ── Categories ────────────────────────────────────────────────────────────────
categories_router = APIRouter(prefix="/categories", tags=["Categorias"])


@categories_router.get("", response_model=list[CategoryResponse])
async def list_categories(type: str | None = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CategoryService(db).list(current_user.id, type=type)


@categories_router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CategoryService(db).create(current_user.id, data)


@categories_router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: str, data: CategoryUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CategoryService(db).update(current_user.id, category_id, data)


@categories_router.delete("/{category_id}", response_model=MessageResponse)
async def delete_category(category_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await CategoryService(db).delete(current_user.id, category_id)
    return MessageResponse(message="Categoria removida com sucesso.")


# ── Goals ─────────────────────────────────────────────────────────────────────
goals_router = APIRouter(prefix="/goals", tags=["Metas"])


@goals_router.get("", response_model=list[GoalResponse])
async def list_goals(status: str | None = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GoalService(db).list(current_user.id, status=status)


@goals_router.post("", response_model=GoalResponse, status_code=201)
async def create_goal(data: GoalCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GoalService(db).create(current_user.id, data)


@goals_router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: str, data: GoalUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await GoalService(db).update(current_user.id, goal_id, data)


@goals_router.delete("/{goal_id}", response_model=MessageResponse)
async def delete_goal(goal_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await GoalService(db).delete(current_user.id, goal_id)
    return MessageResponse(message="Meta removida com sucesso.")


# ── Notifications ─────────────────────────────────────────────────────────────
notifications_router = APIRouter(prefix="/notifications", tags=["Notificações"])


@notifications_router.get("", response_model=list[NotificationResponse])
async def list_notifications(unread_only: bool = Query(False), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await NotificationService(db).list(current_user.id, unread_only=unread_only)


@notifications_router.patch("/read", response_model=MessageResponse)
async def mark_read(data: NotificationMarkRead, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await NotificationService(db).mark_read(current_user.id, data.ids)
    return MessageResponse(message="Notificações marcadas como lidas.")