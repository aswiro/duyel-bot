from aiogram.fsm.state import State, StatesGroup


class DuelSG(StatesGroup):
    main_menu = State()
    language_menu = State()
    support_menu = State()
    games_menu = State()
    my_games_menu = State()
    create_game = State()
    insufficient_balance = State()
    max_games_reached = State()


class GameRoom(StatesGroup):
    game_room = State()
    game_room_waiting = State()
    game_room_playing = State()
    game_room_finished = State()
    game_room_ended = State()
