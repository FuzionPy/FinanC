from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.user import UserChangePassword, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Retorna o perfil do usuário autenticado."""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Atualiza nome ou email do usuário."""
    service = UserService(db)
    return await service.update_profile(current_user.id, data)


@router.patch("/me/password", response_model=MessageResponse)
async def change_password(
    data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Altera a senha do usuário autenticado."""
    service = UserService(db)
    await service.change_password(current_user.id, data)
    return MessageResponse(message="Senha alterada com sucesso.")