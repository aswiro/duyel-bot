import enum


# --- Определение Enum-типов для PostgreSQL ---
# Это лучший способ для работы со статусами, так как обеспечивает целостность данных на уровне БД


class GameStatusEnum(enum.Enum):
    pending = "pending"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class TransactionTypeEnum(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    stake = "stake"
    win = "win"
    referral_bonus = "referral_bonus"


class WithdrawalStatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    completed = "completed"
    rejected = "rejected"


class GameTypeEnum(enum.Enum):
    dice = "dice"
    darts = "darts"
    basketball = "basketball"
    football = "football"
    slot = "slot"
    bowling = "bowling"
