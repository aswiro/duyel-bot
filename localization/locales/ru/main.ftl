# --- Общие ---
back-to-menu = ⬅️ Назад в меню
balance = 💰 Баланс: ${$balance}
change-language = 🌐 Изменить язык
language-changed = ✅ Язык успешно изменен!
choose-language = 🌐 Выберите ваш язык:
support = 💬 Поддержка
support-title = 💬 Поддержка
contact-admin = 📞 Связаться с администратором
faq = ❓ Часто задаваемые вопросы
contact-admin-message = 📞 Для связи с администратором напишите @admin
faq-message = ❓ Часто задаваемые вопросы:
1. Как начать работу?
2. Как создать кампанию?
3. Как пополнить баланс?

# --- Главное меню ---
main-menu-welcome = 👋 Добро пожаловать, {$user_name}!
games-menu = 🎮 Меню игр

# --- Меню игр ---
games-welcome = Привет, { $user_name }! Ваш баланс: ${ $balance }
games-list = 📜 Список доступных игр
no-pending-games = 😔 Нет доступных игр для присоединения.
my-games = 🕹️ Мои игры
create-game = ✨ Создать игру
game-history = 📊 История игр
game-not-available-error = ⚠️ Эта игра больше не доступна.
cannot-join-own-game-error = 🚫 Вы не можете присоединиться к своей собственной игре.
insufficient-balance-for-join = 😔 Недостаточно средств для присоединения к этой игре.

# --- Создание игры ---
enter-stake = 💰 Введите сумму ставки (от 5 до 10000):
invalid-stake-format = ⚠️ Неверный формат ставки. Введите число.
stake-must-be-positive = 🚫 Ставка должна быть положительной.
stake-must-be-at-least-5 = 💰 Минимальная ставка: 5.
stake-too-large = 💰 Максимальная ставка: 10000.
insufficient-balance-for-stake = 😔 Недостаточно средств для такой ставки.
insufficient-balance-for-create = 😔 Недостаточно средств для создания игры.
max-games-reached = 🚫 Вы достигли лимита активных игр (5).
game-created-success = ✅ Игра создана!
    .type = { $game_emoji } Тип: { $game_type }
    .stake = 💵 Ставка: { $stake }
    .rolls = 🎲 Бросков: { $rolls }
game-creation-error = ❌ Ошибка при создании игры.

# --- Мои Игры ---
my-games-title = 🎯 Мои игры
no-active-games = 😔 У вас нет активных игр.
game-info = 💎 #{$game_id} | {$game_emoji} | Ставка: ${$stake} | Статус: {$status}
cancel-game = ❌ Отменить игру
confirm-cancel = ❓ Вы уверены, что хотите отменить игру #{$game_id}?
game-cancelled = ✅ Игра #{$game_id} отменена.
cancel-error = ❌ Не удалось отменить игру.

# --- Игровая комната ---
game-header = { $game_emoji } Игра #{ $game_id }
game-bank = 🏦 Банк: ${$bank}
player-info = { $player } | Счет: { $score } | Броски: { $rolls }
turn-of-player = 👉 Ход игрока { $player }
roll-dice-button = 🎲 Бросить кости
game-over = 🏁 Игра окончена!
winner-is = 🏆 Победитель: { $winner }!
your-prize = 💰 Ваш выигрыш: ${ $prize }
no-winner = 🤝 Ничья!
waiting-for-opponent = ⏳ Ожидание второго игрока...
game-start-notification = 🚀 Игра #{ $game_id } началась!
roll-notification = { $player } бросил кости и получил { $roll_value }.
your-turn-notification = 👉 Ваш ход в игре #{ $game_id }!
not-your-turn = 🚫 Сейчас не ваш ход.
