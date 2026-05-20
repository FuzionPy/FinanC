from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# ── Hashing de senha ──────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Gera hash bcrypt da senha."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha bate com o hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT ───────────────────────────────────────────────────────────────────────

def _create_token(
    subject: str | Any,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: dict | None = None,
) -> str:
    """
    Função interna que monta e assina qualquer token JWT.

    Parâmetros:
        subject     → normalmente o user_id (convertido para str)
        token_type  → "access" ou "refresh"
        expires_delta → quanto tempo o token é válido
        extra_claims  → claims adicionais opcionais (ex: role)
    """
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(
    subject: str | Any,
    extra_claims: dict | None = None,
) -> str:
    """Cria um access token JWT (curta duração)."""
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        extra_claims=extra_claims,
    )


def create_refresh_token(subject: str | Any) -> str:
    """Cria um refresh token JWT (longa duração)."""
    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decodifica e valida um token JWT.

    Lança:
        JWTError → token inválido ou expirado
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )


def verify_access_token(token: str) -> dict[str, Any]:
    """
    Valida que o token é do tipo 'access' e retorna o payload.

    Lança:
        JWTError → se inválido, expirado ou tipo errado
    """
    try:
        payload = decode_token(token)
    except JWTError:
        raise

    if payload.get("type") != "access":
        raise JWTError("Token inválido: tipo incorreto.")

    return payload


def verify_refresh_token(token: str) -> dict[str, Any]:
    """
    Valida que o token é do tipo 'refresh' e retorna o payload.

    Lança:
        JWTError → se inválido, expirado ou tipo errado
    """
    try:
        payload = decode_token(token)
    except JWTError:
        raise

    if payload.get("type") != "refresh":
        raise JWTError("Token inválido: tipo incorreto.")

    return payload