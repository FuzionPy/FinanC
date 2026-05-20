import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.session import engine
from app.db.base import Base

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação FastAPI.

    Tudo antes do `yield` roda no STARTUP.
    Tudo depois do `yield` roda no SHUTDOWN.

    Uso no main.py:
        app = FastAPI(lifespan=lifespan)
    """
    # ── STARTUP ──────────────────────────────────────────────────────────────
    logger.info("🚀 Iniciando %s v%s...", settings.app_name, settings.app_version)
    logger.info("📦 Ambiente: %s", settings.environment)

    if settings.is_sqlite:
        logger.info("🗄️  Banco: SQLite (desenvolvimento)")
    else:
        logger.info("🗄️  Banco: PostgreSQL (produção)")

    # Em desenvolvimento com SQLite, cria as tabelas automaticamente.
    # Em produção, as tabelas são gerenciadas pelo Alembic (migrations).
    if settings.is_development and settings.is_sqlite:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tabelas SQLite verificadas/criadas.")

    logger.info("✅ Aplicação pronta.")

    yield  # ← aplicação rodando

    # ── SHUTDOWN ─────────────────────────────────────────────────────────────
    logger.info("🛑 Encerrando aplicação...")
    await engine.dispose()
    logger.info("🛑 Conexões com banco encerradas.")