import random

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import BgManagerFactory, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from database import UnitOfWork
from database.models import GameStatusEnum
from utils import decimal_to_float

from ..constants import GAME_EMOJIS
from ..states import GameRoom


async def get_game_room_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для диалога игровой комнаты."""
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    l10n = dialog_manager.middleware_data["l10n"]
    current_user_id = dialog_manager.event.from_user.id
    game_id = dialog_manager.dialog_data.get("game_id")

    async with uow:
        game = await uow.game_service.get_game(game_id)
        if not game:
            # TODO: Handle game not found case
            return {"error": "Game not found"}

        player1_rolls = [r.roll_value for r in game.rolls if r.user_id == game.player1_id]
        player2_rolls = [r.roll_value for r in game.rolls if r.user_id == game.player2_id]
        player1_score = sum(player1_rolls)
        player2_score = sum(player2_rolls)

        # Определяем чей ход
        current_player_id = None
        if len(player1_rolls) < game.rolls_count:
            current_player_id = game.player1_id
        elif len(player2_rolls) < game.rolls_count:
            current_player_id = game.player2_id

        is_my_turn = current_player_id == current_user_id
        is_game_over = current_player_id is None

        # Форматируем данные для вывода
        player1_id_masked = f"***{str(game.player1_id)[-4:]}"
        player2_id_masked = f"***{str(game.player2_id)[-4:]}"
        game_emoji = GAME_EMOJIS.get(game.game_type, "❓")

        turn_text = ""
        if not is_game_over:
            current_player_masked = (
                player1_id_masked if current_player_id == game.player1_id else player2_id_masked
            )
            turn_text = l10n.format_value("turn-of-player", {"player": current_player_masked})

    return {
        "l10n_game_header": l10n.format_value(
            "game-header", {"game_id": game_id, "game_emoji": game_emoji}
        ),
        "l10n_bank": l10n.format_value("game-bank", {"bank": decimal_to_float(game.bank_amount)}),
        "player1_info": l10n.format_value(
            "player-info",
            {
                "player": player1_id_masked,
                "score": player1_score,
                "rolls": " ".join(map(str, player1_rolls)),
            },
        ),
        "player2_info": l10n.format_value(
            "player-info",
            {
                "player": player2_id_masked,
                "score": player2_score,
                "rolls": " ".join(map(str, player2_rolls)),
            },
        ),
        "turn_text": turn_text,
        "is_my_turn": is_my_turn,
        "is_game_over": is_game_over,
        "l10n_roll_dice": l10n.format_value("roll-dice-button"),
        "l10n_game_over": l10n.format_value("game-over"),
        "l10n_back_to_menu": l10n.format_value("back-to-menu"),
    }


async def on_roll_dice_clicked(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """Обработчик нажатия на кнопку 'Бросить кости'."""
    await callback.answer()  # Убираем "часики" на кнопке
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    l10n = dialog_manager.middleware_data["l10n"]
    bot: Bot = dialog_manager.middleware_data["bot"]
    bg_manager_factory: BgManagerFactory = dialog_manager.middleware_data[
        "bg_manager_factory"
    ]
    current_user_id = callback.from_user.id
    game_id = dialog_manager.dialog_data.get("game_id")

    async with uow:
        game = await uow.game_service.get_game(game_id)

        # --- Валидация хода ---
        player1_rolls = [r for r in game.rolls if r.user_id == game.player1_id]
        player2_rolls = [r for r in game.rolls if r.user_id == game.player2_id]

        if len(player1_rolls) + len(player2_rolls) >= game.rolls_count * 2:
            return  # Игра уже окончена

        current_turn_player_id = (
            game.player1_id
            if len(player1_rolls) <= len(player2_rolls)
            else game.player2_id
        )

        if current_turn_player_id != current_user_id:
            await callback.answer(l10n.format_value("not-your-turn"), show_alert=True)
            return

        # --- Совершение броска ---
        roll_value = random.randint(1, 6)
        await uow.roll_service.create_roll(
            game_id=game_id, user_id=current_user_id, roll_value=roll_value
        )
        await uow.commit()

    # --- Обновление диалогов и уведомления ---
    other_player_id = (
        game.player2_id if current_user_id == game.player1_id else game.player1_id
    )

    # Обновляем свой диалог
    await dialog_manager.switch_to(GameRoom.game_room)

    # Обновляем диалог оппонента
    opponent_manager = bg_manager_factory.bg(
        bot=bot, user_id=other_player_id, chat_id=other_player_id
    )
    await opponent_manager.switch_to(GameRoom.game_room)

    # Уведомляем оппонента о броске
    player_masked = f"***{str(current_user_id)[-4:]}"
    await bot.send_message(
        chat_id=other_player_id,
        text=l10n.format_value(
            "roll-notification",
            {"player": player_masked, "roll_value": roll_value},
        ),
    )

    # Проверяем, не закончилась ли игра после этого хода, и если да, то финализируем ее
    async with uow:
        game_after_roll = await uow.game_service.get_game(game_id)
        is_game_over_after_roll = len(game_after_roll.rolls) >= game.rolls_count * 2

        if is_game_over_after_roll:
            # --- Определение победителя и выплата ---
            p1_score = sum(
                r.roll_value
                for r in game_after_roll.rolls
                if r.user_id == game.player1_id
            )
            p2_score = sum(
                r.roll_value
                for r in game_after_roll.rolls
                if r.user_id == game.player2_id
            )

            winner_id = None
            if p1_score > p2_score:
                winner_id = game.player1_id
            elif p2_score > p1_score:
                winner_id = game.player2_id

            if winner_id:
                prize = game.bank_amount - game.commission_amount
                winner_user = await uow.user_service.get_user(winner_id)
                balance_before = winner_user.balance
                new_balance = balance_before + prize
                await uow.user_service.update_user(
                    winner_id, {"balance": new_balance, "wins": winner_user.wins + 1}
                )
                await uow.transaction_service.create_transaction(
                    user_id=winner_id,
                    game_id=game_id,
                    type="credit_win",
                    amount=prize,
                    balance_before=balance_before,
                    balance_after=new_balance,
                )
                await uow.game_service.update_game(
                    game_id,
                    {"status": GameStatusEnum.completed, "winner_id": winner_id},
                )
                winner_masked = f"***{str(winner_id)[-4:]}"
                await bot.send_message(
                    game.player1_id,
                    l10n.format_value("winner-is", {"winner": winner_masked}),
                )
                await bot.send_message(
                    game.player2_id,
                    l10n.format_value("winner-is", {"winner": winner_masked}),
                )

            else:  # Ничья
                stake_refund = game.bank_amount / 2
                p1 = await uow.user_service.get_user(game.player1_id)
                p2 = await uow.user_service.get_user(game.player2_id)
                await uow.user_service.update_user(
                    p1.id, {"balance": p1.balance + stake_refund}
                )
                await uow.user_service.update_user(
                    p2.id, {"balance": p2.balance + stake_refund}
                )
                await uow.game_service.update_game(
                    game_id, {"status": GameStatusEnum.completed}
                )
                await bot.send_message(game.player1_id, l10n.format_value("no-winner"))
                await bot.send_message(game.player2_id, l10n.format_value("no-winner"))

            await uow.commit()

        else:  # Если игра не окончена, уведомляем о следующем ходе
            await bot.send_message(
                chat_id=other_player_id,
                text=l10n.format_value("your-turn-notification", {"game_id": game_id}),
            )


game_room_window = Window(
    Format("{l10n_game_header}"),
    Format("{l10n_bank}"),
    Const(""),
    Format("{player1_info}"),
    Format("{player2_info}"),
    Const(""),
    Format("{turn_text}", when="not is_game_over"),
    Format("{l10n_game_over}", when="is_game_over"),
    Button(
        Format("{l10n_roll_dice}"),
        id="roll_dice",
        on_click=on_roll_dice_clicked,
        when="is_my_turn and not is_game_over",
    ),
    state=GameRoom.game_room,
    getter=get_game_room_data,
)
