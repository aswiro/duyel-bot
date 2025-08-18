import pytest
from decimal import Decimal
from sqlalchemy.orm import selectinload

from database.models import Game, GameStatusEnum, User
from database.services import GameService, UserService, RollService, TransactionService
from database.unit_of_work import UnitOfWork

# Мы будем использовать pytest-asyncio, поэтому помечаем тесты как асинхронные
pytestmark = pytest.mark.asyncio


async def test_full_game_lifecycle(test_uow: UnitOfWork):
    """
    Тестирует полный жизненный цикл игры:
    1. Создание игры игроком 1.
    2. Присоединение игрока 2.
    3. Симуляция бросков.
    4. Определение победителя и выплата.
    """
    user_service = test_uow.user_service
    game_service = test_uow.game_service
    roll_service = test_uow.roll_service
    transaction_service = test_uow.transaction_service

    # --- 1. Создание пользователей через репозиторий для установки баланса ---
    user_repo = test_uow.users
    p1_data = {"id": 100, "first_name": "Player1", "balance": Decimal("100.00")}
    p2_data = {"id": 200, "first_name": "Player2", "balance": Decimal("100.00")}
    await user_repo.create(p1_data)
    await user_repo.create(p2_data)

    p1 = await user_repo.get(100)
    p2 = await user_service.get_user(200)

    initial_p1_balance = p1.balance
    initial_p2_balance = p2.balance
    stake = Decimal("10.00")

    # --- 2. Игрок 1 создает игру ---
    game_data = {
        "player1_id": p1.id,
        "stake_amount": stake,
        "bank_amount": stake * 2,
        "commission_amount": (stake * 2) * Decimal("0.1"),
        "rolls_count": 1,  # Для простоты теста
    }
    created_game = await game_service.create_game(game_data)
    await user_service.update_user(p1.id, {"balance": p1.balance - stake})

    # Проверка после создания
    await test_uow.session.flush() # Flush to get DB-generated values without committing
    p1_after_creation = await user_service.get_user(p1.id)
    assert p1_after_creation.balance == initial_p1_balance - stake
    assert created_game.status == GameStatusEnum.pending
    assert created_game.player1_id == p1.id

    # --- 3. Игрок 2 присоединяется к игре ---
    await game_service.update_game(
        created_game.id, {"player2_id": p2.id, "status": GameStatusEnum.active}
    )
    await user_service.update_user(p2.id, {"balance": p2.balance - stake})

    # Проверка после присоединения
    await test_uow.session.flush()
    game_after_join = await game_service.get_game(created_game.id)
    p2_after_join = await user_service.get_user(p2.id)
    assert p2_after_join.balance == initial_p2_balance - stake
    assert game_after_join.status == GameStatusEnum.active
    assert game_after_join.player2_id == p2.id

    # --- 4. Симуляция бросков (P1 бросает 6, P2 бросает 1) ---
    await roll_service.create_roll(
        {"game_id": game_after_join.id, "user_id": p1.id, "roll_value": 6}
    )
    await roll_service.create_roll(
        {"game_id": game_after_join.id, "user_id": p2.id, "roll_value": 1}
    )

    # --- 5. Финализация игры и выплата ---
    # В реальном коде это внутри on_roll_dice_clicked, здесь симулируем
    game_with_rolls = await game_service.get_game(
        game_after_join.id, options=[selectinload(Game.rolls)]
    )
    p1_score = sum(r.roll_value for r in game_with_rolls.rolls if r.user_id == p1.id)
    p2_score = sum(r.roll_value for r in game_with_rolls.rolls if r.user_id == p2.id)

    assert p1_score > p2_score
    winner_id = p1.id
    loser_id = p2.id

    prize = game_with_rolls.bank_amount - game_with_rolls.commission_amount
    winner_before_payout = await user_service.get_user(winner_id)

    # Обновляем баланс победителя и статус игры
    await user_service.update_user(
        winner_id, {"balance": winner_before_payout.balance + prize}
    )
    await game_service.update_game(
        game_with_rolls.id, {"status": GameStatusEnum.completed, "winner_id": winner_id}
    )

    # --- 6. Финальные проверки ---
    # The commit happens automatically on fixture teardown, so we can fetch final state
    p1_final = await user_service.get_user(p1.id)
    p2_final = await user_service.get_user(p2.id)
    final_game = await game_service.get_game(game_after_join.id)

    # Баланс победителя: начальный - ставка + выигрыш
    expected_p1_balance = initial_p1_balance - stake + prize
    assert p1_final.balance == expected_p1_balance
    # Баланс проигравшего: начальный - ставка
    assert p2_final.balance == initial_p2_balance - stake

    assert final_game.status == GameStatusEnum.completed
    assert final_game.winner_id == p1.id
