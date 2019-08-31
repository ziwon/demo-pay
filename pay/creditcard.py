import logging.config
from typing import ClassVar
from dataclasses import dataclass

from pay.logging import LOG


@dataclass
class CreditCard:
    name: str
    card_number: int
    balance: int = 0
    limit: int = 0

    INVALID_CREDIT_CARD_NUMBER: ClassVar[str] = "error"

    def __post_init__(self) -> None:
        if not self.luhn_valid(self.card_number):
            LOG.warn(f"Invalid card number: {self.card_number}")

    @staticmethod
    def luhn_valid(card_number) -> bool:
        r = [int(ch) for ch in str(card_number)][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

    def charge(self, amount) -> bool:
        if not self.luhn_valid(self.card_number):
            LOG.warn(f"Invalid card number: {self.card_number}")
            self.balance = CreditCard.INVALID_CREDIT_CARD_NUMBER
            return False

        if self.balance + amount > self.limit:
            LOG.warn(
                f"Charging ${amount} to balance ${self.balance} is exceeded the limit: ${self.limit}"
            )
            return False

        self.balance += amount

        return True

    def credit(self, amount) -> bool:
        if not self.luhn_valid(self.card_number):
            LOG.warn(f"Invalid card number: {self.card_number}")
            self.balance = CreditCard.INVALID_CREDIT_CARD_NUMBER
            return False

        self.balance -= amount
        return True

    def get_status(self) -> str:
        return f"{self.name}: ${self.balance}"
