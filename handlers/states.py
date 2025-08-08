from aiogram.fsm.state import State, StatesGroup


class DuelSG(StatesGroup):
    main_menu = State()
    language_menu = State()
    support_menu = State()
    games_menu = State()
    my_games_menu = State()
    create_game = State()
