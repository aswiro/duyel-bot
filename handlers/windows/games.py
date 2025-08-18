"""Диалог игр."""

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from decimal import Decimal

from aiogram import Bot
from aiogram_dialog import BgManagerFactory

from database import UnitOfWork
from database.models import GameStatusEnum
from utils import decimal_to_float as dtf

from ..states import DuelSG, GameRoom
from ..widgets import GamesWindowWidgets


async def get_games_data(dialog_manager, **kwargs):
    """Получает данные для диалога игр."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id
    full_name = dialog_manager.event.from_user.full_name

    # Получаем список игр со статусом pending
    async with uow:
        user = await uow.user_service.get_user(user_id)
        pending_games = await uow.game_service.get_other_user_games(
            user_id=user_id,
        )

    # Форматируем игры для отображения
    games_list = []
    for game in pending_games:
        games_list.append(
            {
                "id": str(game.id),
                "name": f"Игра #{game.id}",
                "stake": f"{dtf(game.stake_amount):.2f} USD.",
            }
        )

    return {
        "user_name": full_name,
        "balance": f"{dtf(user.balance):.2f} USD.",
        "games": games_list,
        "has_games": len(games_list) > 0,
        "games-welcome": l10n.format_value(
            "games-welcome",
            {"user_name": full_name, "balance": dtf(user.balance)},
        ),
        "games-list": l10n.format_value("games-list"),
        "no-pending-games": l10n.format_value("no-pending-games"),
        "l10n_my_games": l10n.format_value("my-games"),
        "game-history": l10n.format_value("game-history"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_game_selected(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    game_id: str,
):
    """Обработчик выбора игры и присоединения к ней."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = callback.from_user.id
    game_id_int = int(game_id)

    async with uow:
        game = await uow.game_service.get_game(game_id_int)
        user = await uow.user_service.get_user(user_id)

        # --- Валидация ---
        if not game or game.status != GameStatusEnum.pending:
            await callback.answer(
                l10n.format_value("game-not-available-error"), show_alert=True
            )
            await dialog_manager.switch_to(DuelSG.games_menu)
            return

        if game.player1_id == user_id:
            await callback.answer(
                l10n.format_value("cannot-join-own-game-error"), show_alert=True
            )
            return

        if user.balance < game.stake_amount:
            await callback.answer(
                l10n.format_value("insufficient-balance-for-join"), show_alert=True
            )
            return

        # --- Обновление состояния ---
        # Обновляем игру
        await uow.game_service.update_game(
            game_id_int,
            {"player2_id": user_id, "status": GameStatusEnum.active},
        )

        # Списываем ставку со второго игрока
        new_balance = user.balance - game.stake_amount
        await uow.user_service.update_user(user_id, {"balance": new_balance})

        # Создаем транзакцию для второго игрока
        await uow.transaction_service.create_transaction(
            user_id=user_id,
            game_id=game_id_int,
            type="debit_stake",
            amount=game.stake_amount,
            balance_before=user.balance,
            balance_after=new_balance,
            description=f"Ставка в игре #{game_id_int}",
        )

        await uow.commit()

    # --- Переход в игровую комнату ---
    dialog_manager.dialog_data.update({"game_id": game_id_int})
    await dialog_manager.switch_to(GameRoom.game_room)

    # Уведомляем и переводим в комнату первого игрока
    bg_manager_factory: BgManagerFactory = dialog_manager.middleware_data[
        "bg_manager_factory"
    ]
    bot: Bot = dialog_manager.middleware_data["bot"]
    player1_manager = bg_manager_factory.bg(
        bot=bot, user_id=game.player1_id, chat_id=game.player1_id
    )
    await player1_manager.start(
        GameRoom.game_room, data={"game_id": game_id_int},
    )


games_window = Window(
    Format("{games-welcome}"),
    Format("{games-list}:", when="has_games"),
    Column(
        Select(
            Format("🎮 {item[name]} - Ставка: {item[stake]}"),
            id="game_id",
            item_id_getter=lambda item: str(item["id"]),
            items="games",
            on_click=on_game_selected,
        ),
        when="has_games",
    ),
    Format("{no-pending-games}", when=~F["has_games"]),
    Column(
        GamesWindowWidgets.my_games_button(),
        Button(
            Format("{game-history}"),
            "game_history",
            on_click=lambda c, w, m: c.answer("История игр будет добавлена позже"),
        ),
    ),
    GamesWindowWidgets.back_button(DuelSG.main_menu),
    parse_mode="HTML",
    state=DuelSG.games_menu,
    getter=get_games_data,
)
