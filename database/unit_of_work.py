# database/unit_of_work.py
"""
Unit of Work Pattern для управления транзакциями
"""

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import (
    UserRepository,
    GameRepository,
    RollRepository,
    TransactionRepository,
    WithdrawalRequestRepository,
)
from .services import (
    UserService,
    GameService,
    RollService,
    TransactionService,
    WithdrawalRequestService,
)


class UnitOfWork:
    """Unit of Work для управления транзакциями"""

    def __init__(self, session: AsyncSession):
        self.session = session

        # Repositories
        self.users = UserRepository(session)
        self.games = GameRepository(session)
        self.rolls = RollRepository(session)
        self.transactions = TransactionRepository(session)
        self.withdrawal_requests = WithdrawalRequestRepository(session)

        # Services
        self.user_service = UserService(session)
        self.game_service = GameService(session)
        self.roll_service = RollService(session)
        self.transaction_service = TransactionService(session)
        self.withdrawal_request_service = WithdrawalRequestService(session)

    async def commit(self):
        """Коммит транзакции"""
        await self.session.commit()

    async def rollback(self):
        """Откат транзакции"""
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
