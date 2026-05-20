from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações centrais da aplicação.
    Lidas automaticamente do arquivo .env via pydantic-settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Ambiente ─────────────────────────────────────────────────────────────
    environment: Literal["development", "production"] = "development"
    debug: bool = False

    # ── Aplicação ─────────────────────────────────────────────────────────────
    app_name: str = "FinanC"
    app_version: str = "0.1.0"

    # ── Banco de Dados ────────────────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./fincontrol.db"

    # ── JWT ───────────────────────────────────────────────────────────────────
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ── CORS ──────────────────────────────────────────────────────────────────
    allowed_origins: list[str] = ["http://localhost:5173"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: str | list[str]) -> list[str]:
        """Aceita tanto string separada por vírgula quanto lista."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ── Propriedades utilitárias ──────────────────────────────────────────────

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return self.database_url.startswith("postgresql")

    @property
    def async_database_url(self) -> str:
        """
        Garante que a URL use drivers async:
          sqlite   → sqlite+aiosqlite
          postgres → postgresql+asyncpg
        """
        url = self.database_url

        if url.startswith("sqlite://") and "aiosqlite" not in url:
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)

        if url.startswith("postgresql://") and "asyncpg" not in url:
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Railway injeta DATABASE_URL com prefixo "postgres://" (sem ql)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)

        return url


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância singleton de Settings.
    O @lru_cache garante que o .env seja lido apenas uma vez.

    Uso:
        from app.core.config import get_settings
        settings = get_settings()
    """
    return Settings()