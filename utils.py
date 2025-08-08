"""Утилиты для работы с данными."""

import json
from decimal import Decimal
from typing import Any


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder для корректной сериализации Decimal значений."""
    
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def decimal_to_float(value: Decimal | float | int) -> float:
    """Конвертирует Decimal в float для совместимости."""
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def ensure_decimal(value: float | int | str | Decimal) -> Decimal:
    """Конвертирует значение в Decimal для точных вычислений."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def format_money(amount: Decimal | float | int, currency: str = "$") -> str:
    """Форматирует денежную сумму для отображения."""
    if isinstance(amount, Decimal):
        return f"{currency}{amount:.2f}"
    return f"{currency}{amount:.2f}"