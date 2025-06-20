import enum

class WalletTransactionType(enum.Enum):
    DEPOSIT = "deposit"
    SPEND = "spend"

class WalletTransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
