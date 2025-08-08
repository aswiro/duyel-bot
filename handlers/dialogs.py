from aiogram_dialog import Dialog

from .windows import (
    games_window,
    language_window,
    main_window,
    my_games_window,
    support_window,
    create_game_window,
)


main_dialog = Dialog(
    main_window,
    language_window,
    support_window,
    games_window,
    my_games_window,
    create_game_window,
)
