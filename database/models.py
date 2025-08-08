from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base, relationship

from database.status import (
    GameStatusEnum,
    GameTypeEnum,
    TransactionTypeEnum,
    WithdrawalStatusEnum,
)

# --- Базовая настройка SQLAlchemy ---
Base = declarative_base()


# --- Модели данных ---


class User(Base):
    """
    Модель Пользователя. Хранит всю информацию о зарегистрированных пользователях,
    включая их баланс и реферальную связь.
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, nullable=False, index=True)
    username = Column(String(30), nullable=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=True)
    phone = Column(String(15), nullable=True)
    language_code = Column(String(2), nullable=True)

    balance = Column(Numeric(15, 2), nullable=False, server_default="0.00")
    wins = Column(Integer, nullable=False, server_default="0")
    losses = Column(Integer, nullable=False, server_default="0")

    # Реферальная система
    referrer_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи (Relationships)
    referrer = relationship("User", remote_side=[id], backref="referrals")

    # Связи с другими таблицами
    transactions = relationship("Transaction", back_populates="user")
    withdrawal_requests = relationship("WithdrawalRequest", back_populates="user")
    referral_earnings = relationship(
        "ReferralEarning",
        foreign_keys="[ReferralEarning.referrer_id]",
        back_populates="referrer_user",
    )

    def __repr__(self):
        return f"<User(id={self.id}, balance={self.balance})>"


# --------------------------------------------------------------------------------------


class Game(Base):
    """
    Модель Игры. Хранит информацию о каждой игровой сессии, ставках и результате.
    """

    __tablename__ = "games"

    id = Column(BigInteger, primary_key=True)
    game_type = Column(
        ENUM(GameTypeEnum, name="game_type_enum"),
        nullable=False,
        default=GameTypeEnum.dice,
    )
    player1_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    player2_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    winner_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    stake_amount = Column(Numeric(15, 2), nullable=False)
    bank_amount = Column(Numeric(15, 2), nullable=False)
    commission_amount = Column(Numeric(15, 2), nullable=False, server_default="1.00")
    rolls_count = Column(Integer, nullable=False, server_default="3")

    status = Column(
        ENUM(GameStatusEnum, name="game_status_enum"),
        nullable=False,
        default=GameStatusEnum.pending,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    comment = Column(Text, nullable=True)

    # Связи
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])

    rolls = relationship("Roll", back_populates="game")

    def __repr__(self):
        return (
            f"<Game(id={self.id}, status='{self.status}', stake={self.stake_amount})>"
        )


# --------------------------------------------------------------------------------------


class Roll(Base):
    """
    Модель Броска. Логирует каждый бросок игрока в рамках игры.
    """

    __tablename__ = "rolls"

    id = Column(BigInteger, primary_key=True)
    game_id = Column(BigInteger, ForeignKey("games.id"), nullable=False, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    roll_value = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    game = relationship("Game", back_populates="rolls")
    user = relationship("User")

    def __repr__(self):
        return (
            f"<Roll(id={self.id}, game_id={self.game_id}, "
            f"user_id={self.user_id}, roll_value={self.roll_value})>"
        )


# --------------------------------------------------------------------------------------


class Transaction(Base):
    """
    Модель Транзакции. Аудит всех финансовых операций (банковская выписка).
    """

    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    game_id = Column(BigInteger, ForeignKey("games.id"), nullable=True)

    type = Column(
        ENUM(TransactionTypeEnum, name="transaction_type_enum"), nullable=False
    )
    amount = Column(Numeric(15, 2), nullable=False)

    balance_before = Column(Numeric(15, 2), nullable=False)
    balance_after = Column(Numeric(15, 2), nullable=False)

    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User", back_populates="transactions")
    game = relationship("Game")

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, type='{self.type}', amount={self.amount})>"


# --------------------------------------------------------------------------------------


class WithdrawalRequest(Base):
    """
    Модель Заявки на вывод. Используется администратором для обработки выплат.
    """

    __tablename__ = "withdrawal_requests"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)

    amount = Column(Numeric(15, 2), nullable=False)
    status = Column(
        ENUM(WithdrawalStatusEnum, name="withdrawal_status_enum"),
        nullable=False,
        server_default="pending",
    )

    payment_details = Column(
        Text, nullable=False
    )  # ВАЖНО: шифровать эти данные в приложении
    rejection_reason = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Связи
    user = relationship("User", back_populates="withdrawal_requests")

    def __repr__(self):
        return f"<WithdrawalRequest(id={self.id}, user_id={self.user_id}, amount={self.amount}, status='{self.status}')>"


# --------------------------------------------------------------------------------------


class ReferralEarning(Base):
    """
    Модель Реферальных доходов. Логирует все бонусы, начисленные за рефералов.
    """

    __tablename__ = "referral_earnings"

    id = Column(BigInteger, primary_key=True)
    referrer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    referral_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    source_game_id = Column(BigInteger, ForeignKey("games.id"), nullable=True)

    earned_amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    referrer_user = relationship(
        "User", foreign_keys=[referrer_id], back_populates="referral_earnings"
    )
    referral_user = relationship("User", foreign_keys=[referral_id])
    game = relationship("Game")

    def __repr__(self):
        return f"<ReferralEarning(id={self.id}, referrer_id={self.referrer_id}, amount={self.earned_amount})>"
