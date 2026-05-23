from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}