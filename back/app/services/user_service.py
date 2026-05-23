from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BadRequestException,
    EmailAlreadyExistsException,
    NotFoundException,
)
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserChangePassword, UserResponse, UserUpdate


class UserService:

    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def get_profile(self, user_id: str) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário")
        return UserResponse.model_validate(user)

    async def update_profile(self, user_id: str, data: UserUpdate) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário")

        if data.email and data.email != user.email:
            if await self.repo.email_exists(data.email):
                raise EmailAlreadyExistsException()

        updated = await self.repo.update(user, data.model_dump(exclude_none=True))
        return UserResponse.model_validate(updated)

    async def change_password(self, user_id: str, data: UserChangePassword) -> None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("Usuário")

        if not verify_password(data.current_password, user.password):
            raise BadRequestException("Senha atual incorreta.")

        await self.repo.update(user, {"password": hash_password(data.new_password)})