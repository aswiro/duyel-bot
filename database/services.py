from loguru import logger
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Game, GameStatusEnum, Roll, Transaction, User, WithdrawalRequest
from .repository import (
    GameRepository,
    RollRepository,
    TransactionRepository,
    UserRepository,
    WithdrawalRequestRepository,
)


class UserService:
    """Сервис для работы с пользователями - бизнес-логика"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def create_user(self, telegram_user) -> User:
        """Creates a new user from Telegram"""

        # Создаем нового пользователя
        user_data = {
            "id": telegram_user.id,
            "username": telegram_user.username,
            "first_name": telegram_user.first_name,
            "last_name": telegram_user.last_name,
            "language_code": telegram_user.language_code,
            "updated_at": func.now(),
        }
        return await self.user_repo.create(user_data)

    async def update_user(self, user_id: int, update_data: dict) -> User:
        """Обновление пользователя"""
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        # Добавляем время последней активности к данным обновления
        update_data["last_active_at"] = func.now()

        return await self.user_repo.update(user.id, update_data)

    async def get_user(self, user_id: int, text: str = None) -> User | None:
        logger.debug("Start get User data")
        logger.debug(text)
        return await self.user_repo.get(user_id)


class GameService:
    """Сервис для работы с играми - бизнес-логика"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.game_repo = GameRepository(session)

    async def create_game(self, game_data: dict) -> Game:
        """Creates a new game from Telegram"""
        game_data["created_at"] = func.now()
        return await self.game_repo.create(game_data)

    async def get_game(self, game_id: int, options: list = None) -> Game | None:
        return await self.game_repo.get(game_id, options=options)

    async def get_user_games(
        self, user_id: int, status: GameStatusEnum = None
    ) -> list[Game]:
        """Получает список игр пользователя"""
        if status:
            filters = {
                "status": status,
                "player1_id": user_id,
            }
        else:
            filters = {"player1_id": user_id}

        return await self.game_repo.get_multi(filters=filters)

    async def get_other_user_games(self, user_id: int) -> list[Game]:
        """Получает список игр пользователя"""
        return await self.game_repo.get_pending_games_exclude_user(user_id)

    async def update_game(self, game_id: int, update_data: dict) -> Game:
        """Обновление игры"""
        game = await self.game_repo.get(game_id)
        if not game:
            raise ValueError(f"Game with id {game_id} not found")

        # Добавляем время последней активности к данным обновления
        update_data["finished_at"] = func.now()

        return await self.game_repo.update(game.id, update_data)

    async def delete_game(self, game_id: int) -> None:
        """Удаление игры"""
        return await self.game_repo.delete(game_id)


class RollService:
    """Сервис для работы с бросками - бизнес-логика"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.roll_repo = RollRepository(session)

    async def create_roll(self, roll_data: dict) -> Roll:
        """Creates a new roll from Telegram"""
        roll_data["created_at"] = func.now()
        return await self.roll_repo.create(roll_data)

    async def get_roll(self, roll_id: int) -> Roll | None:
        return await self.roll_repo.get(roll_id)

    async def update_roll(self, roll_id: int, update_data: dict) -> Roll:
        """Обновление броска"""
        roll = await self.roll_repo.get(roll_id)
        if not roll:
            raise ValueError(f"Roll with id {roll_id} not found")

        # Добавляем время последней активности к данным обновления
        update_data["finished_at"] = func.now()

        return await self.roll_repo.update(roll.id, update_data)


class TransactionService:
    """Сервис для работы с транзакциями - бизнес-логика"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.transaction_repo = TransactionRepository(session)

    async def create_transaction(self, transaction_data: dict) -> Transaction:
        """Creates a new transaction from Telegram"""
        transaction_data["created_at"] = func.now()
        return await self.transaction_repo.create(transaction_data)

    async def get_transaction(self, transaction_id: int) -> Transaction | None:
        return await self.transaction_repo.get(transaction_id)

    async def update_transaction(
        self, transaction_id: int, update_data: dict
    ) -> Transaction:
        """Обновление транзакции"""
        transaction = await self.transaction_repo.get(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction with id {transaction_id} not found")

        # Добавляем время последней активности к данным обновления
        update_data["finished_at"] = func.now()

        return await self.transaction_repo.update(transaction.id, update_data)


class WithdrawalRequestService:
    """Сервис для работы с запросами на вывод - бизнес-логика"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.withdrawal_request_repo = WithdrawalRequestRepository(session)

    async def create_withdrawal_request(
        self, withdrawal_request_data: dict
    ) -> WithdrawalRequest:
        """Creates a new withdrawal request from Telegram"""
        withdrawal_request_data["created_at"] = func.now()
        return await self.withdrawal_request_repo.create(withdrawal_request_data)

    async def get_withdrawal_request(
        self, withdrawal_request_id: int
    ) -> WithdrawalRequest | None:
        return await self.withdrawal_request_repo.get(withdrawal_request_id)

    async def update_withdrawal_request(
        self, withdrawal_request_id: int, update_data: dict
    ) -> WithdrawalRequest:
        """Обновление запроса на вывод"""
        withdrawal_request = await self.withdrawal_request_repo.get(
            withdrawal_request_id
        )
        if not withdrawal_request:
            raise ValueError(
                f"WithdrawalRequest with id {withdrawal_request_id} not found"
            )

        # Добавляем время последней активности к данным обновления
        update_data["finished_at"] = func.now()

        return await self.withdrawal_request_repo.update(
            withdrawal_request.id, update_data
        )
