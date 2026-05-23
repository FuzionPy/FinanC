# Este arquivo importa todos os models para garantir que o SQLAlchemy
# e o Alembic os reconheçam ao gerar migrations.
#
# IMPORTANTE: sempre que criar um novo model, adicione o import aqui.

from app.db.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.account import Account  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.income import Income  # noqa: F401
from app.models.expense import Expense  # noqa: F401
from app.models.goal import Goal  # noqa: F401
from app.models.notification import Notification  # noqa: F401

__all__ = [
    "Base",
    "User",
    "Account",
    "Category",
    "Income",
    "Expense",
    "Goal",
    "Notification",
]