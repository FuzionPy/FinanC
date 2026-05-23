from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> User:
        if await self.repo.email_exists(data.email):
            raise EmailAlreadyExistsException()

        return await self.repo.create({
            "name": data.name,
            "email": data.email,
            "password": hash_password(data.password),
        })

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InvalidCredentialsException()

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = verify_refresh_token(refresh_token)
        except Exception:
            raise InvalidTokenException()

        user = await self.repo.get_active_by_id(payload["sub"])
        if not user:
            raise InvalidTokenException()

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )