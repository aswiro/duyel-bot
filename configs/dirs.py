from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# # Директории
LOGS_DIR = BASE_DIR / "logs"
LOCALES_DIR = BASE_DIR / "localization/locales"

# # Создаем директории, если они не существуют
LOGS_DIR.mkdir(exist_ok=True)
LOCALES_DIR.mkdir(exist_ok=True)

# Константы для форматов
CONSOLE_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>"
FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} - {message}"
