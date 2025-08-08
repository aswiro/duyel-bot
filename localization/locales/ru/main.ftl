admin-welcome-message =
    👋 Добро пожаловать в админ-панель, {$user_name}!
    🔧 Вы можете управлять пользователями, кампаниями и статистикой.

advertiser-not-found = Рекламодатель не найден

advertiser-menu =
    👋 Добро пожаловать, {$company_name}!

    💰 Баланс: ${$balance}

    Выберите действие:

no-campaigns = У вас пока нет кампаний.

my-campaigns-header = 📋 Мои кампании:

campaign-info =
    📊 Кампания: {$name}
    💰 Бюджет: ${$budget}
    📈 Статус: {$status}
    📅 Создана: {$created_at}

campaign-not-found = Кампания не найдена

campaign-details =
    📊 Детали кампании

    📝 Название: {$name}
    💰 Дневной бюджет: ${$daily_budget}
    💸 Потрачено: ${$spent_amount}
    📈 Статус: {$status}
    📅 Дата начала: {$start_date}
    📅 Дата окончания: {$end_date}
    🕒 Создана: {$created_at}

create-campaign-enter-name = 📝 Введите название кампании:

campaign-name-too-short = ❌ Название кампании слишком короткое. Минимум 3 символа.

campaign-name-too-long = ❌ Название кампании слишком длинное. Максимум 100 символов.

create-campaign-enter-budget = 💰 Введите дневной бюджет (в долларах США):

budget-must-be-positive = ❌ Бюджет должен быть положительным.

budget-too-large = ❌ Бюджет слишком большой. Максимум $10,000 в день.

invalid-budget-format = ❌ Неверный формат бюджета. Пожалуйста, введите число.

create-campaign-enter-start-date = 📅 Выберите дату начала:

create-campaign-enter-end-date = 📅 Выберите дату окончания:

start-date-in-past = ❌ Дата начала не может быть в прошлом.

invalid-date-format = ❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ

end-date-before-start = ❌ Дата окончания не может быть раньше даты начала.

create-campaign-confirmation =
    ✅ Сводка кампании

    📝 Название: {$name}
    💰 Дневной бюджет: ${$budget}
    📅 Дата начала: {$start_date}
    📅 Дата окончания: {$end_date}

    Подтвердить создание?

campaign-created-success = ✅ Кампания '{$name}' успешно создана!

campaign-creation-error = ❌ Ошибка создания кампании. Пожалуйста, попробуйте снова.

admin-ad-menu = 🔧 Админ меню рекламы

moderation-queue-header = 📋 Очередь модерации креативов

no-creatives-pending = Нет креативов, ожидающих модерации.

moderation-error = Ошибка при модерации креатива.

creative-not-found = Креатив не найден.

creative-details-header = 📝 Детали креатива

creative-type = Тип: {$type}

creative-campaign = Кампания: {$campaign}

creative-advertiser = Рекламодатель: {$advertiser}

creative-created = Создан: {$date}

creative-approved-success = ✅ Креатив успешно одобрен!

select-rejection-reason = Выберите причину отклонения:

reason-inappropriate = Неподходящий контент

reason-misleading = Вводящая в заблуждение информация

reason-quality = Плохое качество

reason-policy = Нарушение политики

creative-rejected-success = ❌ Креатив отклонен. Причина: {$reason}

enter-custom-reason = Введите причину отклонения:

no-campaigns-found = ❌ Кампании не найдены

all-campaigns-title = 📊 Все рекламные кампании

total-campaigns = Всего кампаний: {$count}

page-info = Страница {$current} из {$total}

error-occurred = ❌ Произошла ошибка

advertiser_not_found = ❌ Рекламодатель не найден

advertiser_details =
    📊 Рекламодатель: {$name}

    💰 Баланс: {$balance}₽
    📈 Всего кампаний: {$total_campaigns}
    🟢 Активных кампаний: {$active_campaigns}
    💸 Всего потрачено: {$total_spent}₽
    📅 Дата регистрации: {$created_at}

no-advertisers-found = Рекламодатели не найдены

advertisers-management-title = 🏢 Управление рекламодателями

total-advertisers = Всего рекламодателей: {$count}

advertisers-page-info = Страница {$current} из {$total}

captcha-settings-menu = Настройки капчи

setting-updated = Настройки обновлены!

select-captcha-type = Выберите тип капчи

select-captcha-size = Выберите размер капчи

select-captcha-difficulty = Выберите сложность капчи

select-captcha-chars-mode = Режим символов

enter-new-value = Введите новое значение

invalid-numeric-value = ❌ Неверное значение. Пожалуйста, введите корректное число.

error-generating-captcha = ❌ Ошибка получения списка групп.

captcha-preview-caption = Предпросмотр капчи

select_group = 📋 Выберите группу для настройки фильтров:

no-filters-found = ❌ Фильтры для этой группы не найдены.

unknown-group = Неизвестная группа

filters-for-group = 🔧 Фильтры для группы: {$group_name}

filter-updated-success = ✅ Фильтр успешно обновлен для группы: {$group_name}

filter-max-message-length = Максимальная длина сообщения

filter-bonus-per-user = Бонус на пользователя

filter-bonus-checkpoint = Контрольная точка бонуса

enter-value = Введите новое значение для фильтра {$filter_name}. Текущее значение: {$current_value}

invalid-message-length-range = ❌ Неверное значение! Длина сообщения должна быть от 10 до 4000 символов.

invalid-bonus-per-user-range = ❌ Неверное значение! Бонус на пользователя должен быть от 1 до 100 единиц.

invalid-bonus-checkpoint-range = ❌ Неверное значение! Контрольная точка бонуса должна быть от 100 до 10000 единиц.

invalid-number-format = ❌ Неверный формат группы. Пожалуйста, отправьте корректную ссылку на группу или имя пользователя.

filter-update-error = ❌ Ошибка обновления фильтра. Пожалуйста, попробуйте снова.

error-getting-groups = ❌ Ошибка получения списка групп.

groups-list-empty = 📭 Список групп пуст.

all-groups-header = 📋 Все группы:

add-group-instructions =
    Пожалуйста, отправьте мне ссылку на группу или имя пользователя (например, @groupname или
    https://t.me/groupname)

invalid-group-format = ❌ Неверный формат группы. Пожалуйста, отправьте корректную ссылку на группу или имя пользователя.

balance = Баланс
enter-stake = Введите ставку
insufficient-balance-for-create = Недостаточно средств для создания игры.

getting-group-info = 🔍 Получение информации о группе...

getting-admins-list = 👥 Получение списка администраторов...

saving-to-database = 💾 Сохранение в базу данных...

no-username = Нет имени пользователя

group-added-success = ✅ Группа успешно добавлена в мониторинг!

error-chat-not-found = ❌ Чат не найден. Пожалуйста, проверьте ссылку или имя пользователя.

error-bot-not-member =
    ❌ Бот не является участником этой группы. Пожалуйста, сначала добавьте бота в группу.

error-insufficient-rights = ❌ У бота недостаточно прав в этой группе.

error-adding-group = ❌ Ошибка добавления группы. Пожалуйста, попробуйте позже.

error-removing-group = ❌ Ошибка удаления группы.

choose-language = 🌐 Выберите ваш язык:

welcome-message =
    👋 Добро пожаловать, {$user_name}!

    Я бот для мониторинга Telegram групп. Выберите действие из меню
    ниже:

language-changed = ✅ Язык успешно изменен!

my-campaigns = 📋 Мои кампании

create-campaign = ➕ Создать кампанию

my-balance = 💰 Мой баланс

ad-analytics = 📊 Аналитика

edit_advertiser_balance = 💰 Редактировать баланс

view_advertiser_campaigns = 📈 Кампании рекламодателя

block_advertiser = 🚫 Заблокировать

back_to_advertisers = ⬅️ Назад к рекламодателям

back-to-ad-menu = ⬅️ Назад в меню рекламы

campaign-analytics = 📊 Аналитика кампании

show-more-campaigns = 📄 Показать еще

activate-campaign = ▶️ Активировать

pause-campaign = ⏸️ Приостановить

register-advertiser = 🚀 Стать рекламодателем

register-advertiser-enter-name = Введите название вашей компании:

already-advertiser = Вы уже зарегистрированы как рекламодатель!

invalid-company-name = Название компании должно быть от 2 до 100 символов

advertiser-registered-success = 🎉 Поздравляем! Вы успешно зарегистрированы как рекламодатель для '{$company_name}'

advertiser-registration-error = ❌ Ошибка при регистрации. Пожалуйста, попробуйте позже.

resume-campaign = ▶️ Возобновить

edit-campaign = ✏️ Редактировать

campaign-creatives = 🎨 Креативы

back-to-campaigns = ⬅️ Назад к кампаниям

cancel = ❌ Отмена

start-now = 🚀 Начать сейчас

one-week = 📅 Одна неделя

one-month = 📅 Один месяц

confirm-create = ✅ Подтвердить

view-campaign = 👁️ Просмотреть кампанию

moderate-ads = 🔍 Модерировать рекламу

all-campaigns = 📋 Все кампании

advertiser-management = 👥 Управление рекламодателями

ad-analytics-admin = 📊 Аналитика рекламы (Админ)

no-pending-creatives = Нет ожидающих креативов

show-more-creatives = Показать еще креативы

refresh-queue = Обновить очередь

back-to-admin-menu = ⬅️ Назад в админ меню

approve-creative = Одобрить

reject-creative = Отклонить

back-to-moderation = Назад к модерации

inappropriate-content = Неподходящий контент

misleading-info = Вводящая в заблуждение информация

poor-quality = Плохое качество

policy-violation = Нарушение политики

custom-reason = Пользовательская причина

back-to-creative = Назад к креативу

back-to-menu = ⬅️ Назад в меню

# Создание игр
select-game-type = 🎮 Выберите тип игры:

game-type-dice = Кости
game-type-darts = Дартс
game-type-basketball = Баскетбол
game-type-football = Футбол
game-type-slot = Слот
game-type-bowling = Боулинг

balance = Баланс
current-stake = Текущая ставка
enter-stake = 💰 Введите ставку (в долларах):
stake-description = Используйте кнопки +/- или введите сумму от $1 до $10,000
select-rolls = Выберите количество бросков
rolls-description = Выберите 3 или 5 бросков для игры
confirm-game-creation = Подтвердите создание игры
game-details = Детали игры
stake = Ставка
rolls = Броски
confirm = Подтвердить
cancel = Отменить
stake-must-be-positive = ❌ Ставка должна быть положительной
stake-too-large = ❌ Ставка слишком большая. Максимум $10,000
invalid-stake-format = ❌ Неверный формат ставки. Введите число
insufficient-balance = Недостаточно средств на балансе
insufficient-balance-for-stake = Недостаточно средств для данной ставки

enter-rolls = 🎲 Введите количество бросков:
rolls-must-be-positive = ❌ Количество бросков должно быть положительным
rolls-too-many = ❌ Слишком много бросков. Максимум 10
invalid-rolls-format = ❌ Неверный формат. Введите целое число

game-created-success = ✅ Игра создана успешно!
    {$game_emoji} Тип игры: {$game_type}
    💵 Ставка: ${$stake}
    🎲 Бросков: {$rolls}
    💰 Баланс: ${$balance}

game-creation-error = ❌ Ошибка при создании игры. Попробуйте снова

next = ➡️ Далее
back = ⬅️ Назад

change-language = 🌐 Изменить язык

ad-menu = Настройки рекламы

add-group = ➕ Добавить группу

my-groups = 👥 Меню группы

filters-menu = 🔧 Меню фильтров

captcha-type = Тип капчи

captcha-size = Размер капчи

captcha-difficulty = Сложность капчи

easy = Легко

light = Легкий

medium = Средний

hard = Сложный

expert = Эксперт

nightmare = Кошмар

captcha-chars-mode = Режим символов

nums = Цифры

hex = Hex

ascii = ASCII

captcha-multicolor = Многоцветность

captcha-margin = Отступ

captcha-multiplication = Умножение

captcha-timeout = Таймаут

captcha-max-attempts = Максимум попыток

captcha-auto-kick = Автоматическое исключение

preview-captcha = Предпросмотр капчи

back-to-filters = ⬅️ Назад к группам

captcha-type-standard = Стандартная

captcha-type-math = Математическая

back = Назад

filter-hashtag = Хештеги

filter-url = URL ссылки

filter-email = Email адреса

filter-ads = Реклама

filter-phone-number = Номера телефонов

filter-forbidden-words = Запрещенные слова

filter-track-members = Отслеживание участников

filter-captcha = Капча

captcha-settings = Настройки капчи

filter-bonuses-enabled = Бонусная система

back-to-groups = ⬅️ Назад к группам

support = 💬 Поддержка

support-title = 💬 Поддержка

contact-admin = 📞 Связаться с администратором

faq = ❓ Часто задаваемые вопросы

contact-admin-message = 📞 Для связи с администратором напишите @admin

faq-message = ❓ Часто задаваемые вопросы:
1. Как начать работу?
2. Как создать кампанию?
3. Как пополнить баланс?

games-menu = 🎮 Меню игр

games-welcome = 👋 Добро пожаловать, {$user_name}!
    💰 Ваш баланс: {$balance} USD.

games-list = 📋 Список игр

my-games-welcome = 👋 Ваши игры, {$user_name}!
    💰 Ваш баланс: {$balance} USD.

my-games-list = 📋 Доступные игры

my-games = 🎯 Мои игры

no-pending-games = 🚫 Нет доступных игр

create-game = ➕ Создать игру

join-game = 🎮 Присоединиться к игре

game-history = 📊 История игр

back-to-menu = ⬅️ Назад в меню

game-deleted-success = {$game_emoji} Игра #{$game_id} со ставкой {$stake} USD удалена.
        Ваш новый баланс: {$balance} USD.

game-deleted-error = ❌ Ошибка при удалении игры. Попробуйте снова.

stake-must-be-at-least-5 = ❌ Ставка должна быть не менее 5 USD.

max-games-reached = ❌ Вы достигли максимального количества игр (5).

balance = 💰 Баланс
