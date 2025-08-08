from pathlib import Path
from fluent.runtime import FluentLocalization, FluentResourceLoader

# Укажите путь к вашим локалям
from configs import LOCALES_DIR


class FluentDispenser:
    def __init__(self, locales_dir: Path = LOCALES_DIR, default_language: str = "ru"):
        self.__loader = FluentResourceLoader(str(locales_dir) + "/{locale}")
        self.__default_language = default_language
        self.languages = {}

        dirs_names = {item.name for item in locales_dir.iterdir() if item.is_dir()}
        default_language_dir = locales_dir / self.__default_language

        if not default_language_dir.exists():
            raise ValueError("FluentDispenser: default language directory not found")

        ftl_files_list = [
            item.name
            for item in default_language_dir.iterdir()
            if item.suffix == ".ftl"
        ]

        for name in dirs_names:
            if name == default_language:
                self.languages[name] = FluentLocalization(
                    [self.__default_language], ftl_files_list, self.__loader
                )
            else:
                self.languages[name] = FluentLocalization(
                    [name, self.__default_language], ftl_files_list, self.__loader
                )

    @property
    def default_locale(self) -> FluentLocalization:
        return self.languages[self.__default_language]

    @property
    def available_languages(self) -> list[str]:
        return list(self.languages.keys())

    def get_language(self, language_code: str | None) -> FluentLocalization:
        if not language_code:
            return self.default_locale
        return self.languages.get(language_code.split("-")[0], self.default_locale)


# Создаем единственный экземпляр диспенсера
fd = FluentDispenser()
