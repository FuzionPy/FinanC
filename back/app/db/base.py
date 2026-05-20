from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base declarativa para todos os models SQLAlchemy.
    Todos os models do projeto devem herdar desta classe.

    Exemplo:
        from app.db.base import Base

        class User(Base):
            __tablename__ = "users"
            ...
    """
    pass