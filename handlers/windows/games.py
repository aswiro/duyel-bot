"""Диалог игр."""

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Select
from aiogram_dialog.widgets.text import Format

from database import UnitOfWork
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
    callback: CallbackQuery, widget, dialog_manager: DialogManager, game_id: str
):
    """Обработчик выбора игры."""
    # Здесь можно добавить логику присоединения к игре
    await callback.answer(f"Выбрана игра #{game_id}")
    dialog_manager.dialog_data.update({"game_id": game_id})
    await dialog_manager.switch_to(GameRoom.game_room)


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
