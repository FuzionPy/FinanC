from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenException, UnauthorizedException
from app.core.security import verify_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency que extrai e valida o JWT do header Authorization.
    Retorna o usuário autenticado ou lança 401.

    Uso nos endpoints:
        @router.get("/me")
        async def me(user: User = Depends(get_current_user)):
            ...
    """
    try:
        payload = verify_access_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if not user_id:
            raise InvalidTokenException()
    except JWTError:
        raise InvalidTokenException()

    repo = UserRepository(db)
    user = await repo.get_active_by_id(user_id)
    if not user:
        raise UnauthorizedException("Usuário não encontrado ou inativo.")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency que exige que o usuário seja admin."""
    if current_user.role != "admin":
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("Acesso restrito a administradores.")
    return current_user