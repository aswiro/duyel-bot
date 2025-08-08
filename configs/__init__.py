# config/__init__.py
"""Модуль конфигурации приложения.

Этот модуль содержит настройки и конфигурацию для всего приложения,
включая настройки базы данных, Redis, логирования и администраторов.
"""

from .dirs import LOCALES_DIR, LOGS_DIR
from .logger import setup_logger, setup_bot_logger, get_logger
from .settings import Settings, settings


__all__ = [
    "settings",
    "setup_logger",
    "setup_bot_logger",
    "get_logger",
    "Settings",
    "CONSOLE_FORMAT",
    "FILE_FORMAT",
    "LOCALES_DIR",
    "LOGS_DIR",
    "CAPTCHAS_DIR",
]
