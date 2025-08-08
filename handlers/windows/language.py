from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Column, Radio
from aiogram_dialog.widgets.text import Format
from loguru import logger

from configs import LOCALES_DIR
from database.unit_of_work import UnitOfWork

from ..states import DuelSG
from ..widgets import BaseDialogWidgets

# Словарь соответствия кодов языков и их отображения
language_display = {
    "ru": "🇷🇺 Русский",
    "en": "🇺🇸 English",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "it": "🇮🇹 Italiano",
    "pt": "🇵🇹 Português",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
    "ar": "🇸🇦 العربية",
    "hi": "🇮🇳 हिन्दी",
    "tr": "🇹🇷 Türkçe",
    "pl": "🇵🇱 Polski",
    "nl": "🇳🇱 Nederlands",
    "sv": "🇸🇪 Svenska",
    "da": "🇩🇰 Dansk",
    "no": "🇳🇴 Norsk",
    "fi": "🇫🇮 Suomi",
    "cs": "🇨🇿 Čeština",
    "sk": "🇸🇰 Slovenčina",
    "hu": "🇭🇺 Magyar",
    "ro": "🇷🇴 Română",
    "bg": "🇧🇬 Български",
    "hr": "🇭🇷 Hrvatski",
    "sr": "🇷🇸 Српски",
    "sl": "🇸🇮 Slovenščina",
    "et": "🇪🇪 Eesti",
    "lv": "🇱🇻 Latviešu",
    "lt": "🇱🇹 Lietuvių",
    "uk": "🇺🇦 Українська",
    "be": "🇧🇾 Беларуская",
}


def get_available_languages() -> list[str]:
    """Получает список доступных языков из директории локалей."""
    available_languages = []
    if LOCALES_DIR.exists():
        for item in LOCALES_DIR.iterdir():
            if item.is_dir() and item.name != "__pycache__":
                # Проверяем наличие .ftl файлов для Fluent локализации
                ftl_files = list(item.glob("*.ftl"))
                if ftl_files:
                    available_languages.append(item.name)
    available_languages.sort()
    return available_languages


async def get_language_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для языкового диалога."""
    # Получаем текущий язык пользователя
    uow = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id
    current_language = "ru"  # По умолчанию

    async with uow:
        user = await uow.user_service.get_user(user_id)
        if user and user.language_code:
            current_language = user.language_code

    l10n = dialog_manager.middleware_data["l10n"]

    # Получаем данные языков
    radio_widget, languages_data = create_language_radio()

    # Устанавливаем текущий выбранный язык в Radio
    radio_managed = dialog_manager.find("language_radio")
    if radio_managed and current_language:
        await radio_managed.set_checked(current_language)

    return {
        "languages": languages_data,
        "current_language": current_language,
        "l10n_choose_language": l10n.format_value("choose-language"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_language_radio_changed(
    callback: CallbackQuery,
    radio,
    dialog_manager: DialogManager,
    item_id: str,
):
    """Обработчик изменения состояния радио-кнопки языка."""
    # Получаем l10n для локализации сообщения
    l10n = dialog_manager.middleware_data["l10n"]

    # Сразу отвечаем на callback
    await callback.answer(l10n.format_value("language-changed"))

    selected_lang = radio.get_checked()

    if selected_lang:
        # Получаем текущего пользователя
        user_id = callback.from_user.id

        # Получаем зависимости из контекста
        uow: UnitOfWork = dialog_manager.middleware_data["uow"]
        l10n = dialog_manager.middleware_data["l10n"]

        # Сохраняем выбранный язык в базе данных
        async with uow:
            await uow.user_service.update_user(
                user_id, {"language_code": selected_lang}
            )
            await uow.session.commit()

        # Обновляем текущий язык в L10n
        l10n.current_locale = selected_lang

        logger.info(f"Пользователь {user_id} изменил язык на {selected_lang}")

        # Принудительно обновляем интерфейс с новой локализацией
        await dialog_manager.switch_to(
            DuelSG.language_menu,
            show_mode=ShowMode.EDIT,
        )


def create_language_radio():
    """Создает радио-кнопки для выбора языка."""
    available_languages = get_available_languages()
    languages_data = []

    for lang_code in available_languages:
        display_name = language_display.get(lang_code, f"🌐 {lang_code.upper()}")
        languages_data.append((display_name, lang_code))

    return Radio(
        Format("✅  {item[0]}"),  # Отмеченное состояние
        Format("{item[0]}"),  # Неотмеченное состояние
        id="language_radio",
        item_id_getter=lambda item: item[1],
        items="languages",
        on_state_changed=on_language_radio_changed,
    ), languages_data


# Меню для пользователей
language_window = Window(
    Format("{l10n_choose_language}"),
    Column(
        create_language_radio()[0],  # Получаем только Radio виджет
    ),
    BaseDialogWidgets.back_button(DuelSG.main_menu),
    state=DuelSG.language_menu,
    getter=get_language_data,
)
