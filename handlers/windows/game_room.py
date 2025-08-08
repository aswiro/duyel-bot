from aiogram_dialog.widgets.text import Format
from aiogram_dialog.window import Window

from database import UnitOfWork
from database.models import GameStatusEnum
from utils import decimal_to_float

from ..constants import GAME_EMOJIS
from ..states import GameRoom


async def get_game_room_data(dialog_manager, **kwargs):
    """Получает данные для диалога игровой комнаты."""
    uow: UnitOfWork = dialog_manager.middleware_data.get("uow")
    l10n = dialog_manager.middleware_data.get("l10n")
    game_id = dialog_manager.dialog_data.get("game_id")
    async with uow:
        game = await uow.game_service.get_game(game_id)
        player1 = f"***{str(game.player1_id)[-4:]}"
        player2 = f"***{str(game.player2_id)[-4:]}"

        bank = game.bank_amount
        commission = game.commission_amount
        rolls = game.rolls
        game_type = game.game_type
        game_emoji = GAME_EMOJIS.get(game_type, "❓")

        await uow.game_service.update_game(
            game_id,
            {"status": GameStatusEnum.active},
        )

    return {
        "game_id": game_id,
        "game_type": game_type,
        "player1": player1,
        "player2": player2,
        "bank": bank,
        "commission": commission,
        "rolls": rolls,
        "welcome_to_game": l10n.format_value(
            "welcome-to-game",
            {
                "player1": player1,
                "player2": player2,
                "game_bank": decimal_to_float(bank),
                "game_commission": decimal_to_float(commission),
                "game_id": game_id,
                "rolls": rolls,
                "game_type": game_type,
                "game_emoji": game_emoji,
            },
        ),
    }


game_room_window = Window(
    Format("{welcome_to_game}"),
    state=GameRoom.game_room,
    getter=get_game_room_data,
)
