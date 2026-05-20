from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

# ── Engine assíncrona ─────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.debug,           # loga queries SQL em modo debug
    future=True,
    # SQLite não suporta múltiplas conexões simultâneas do mesmo jeito
    # que PostgreSQL, então limitamos o pool em desenvolvimento
    **({"pool_pre_ping": True} if settings.is_postgres else {}),
)

# ── Fábrica de sessões ────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,   # objetos continuam acessíveis após commit
    autocommit=False,
    autoflush=False,
)


# ── Dependency para injeção nas rotas ─────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI que fornece uma sessão de banco por requisição.
    Garante commit em caso de sucesso e rollback em caso de exceção.

    Uso nos endpoints:
        @router.get("/")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise