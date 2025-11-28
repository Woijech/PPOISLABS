from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Protocol

from .enums import PaymentStatus


@dataclass
class Money:
    amount: float
    currency: str = "USD"
    precision: int = 2

    def allocate(self, parts: int) -> float:
        if parts <= 0:
            raise ValueError("Parts must be positive")
        return round(self.amount / parts, self.precision)

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency, self.precision)

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount - other.amount, self.currency, self.precision)

    def percentage(self, percent: float) -> "Money":
        return Money(self.amount * percent / 100.0, self.currency, self.precision)


class PaymentMethod(Protocol):
    def authorize(self, amount: Money) -> bool:
        ...


@dataclass
class CardPayment:
    card_number: str
    holder_name: str
    expiration: str
    billing_address: str = ""

    def authorize(self, amount: Money) -> bool:
        return amount.amount < 10000 and len(self.card_number) in (15, 16)

    def masked_number(self) -> str:
        if len(self.card_number) < 4:
            return "*" * len(self.card_number)
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]


@dataclass
class Payment:
    payment_id: str
    booking_id: str
    amount: Money
    status: PaymentStatus = PaymentStatus.PENDING
    provider: str = "CARD"
    metadata: Dict[str, str] = field(default_factory=dict)

    def mark_completed(self) -> None:
        self.status = PaymentStatus.COMPLETED

    def mark_declined(self) -> None:
        self.status = PaymentStatus.DECLINED

    def mark_refunded(self) -> None:
        self.status = PaymentStatus.REFUNDED

    def is_successful(self) -> bool:
        return self.status == PaymentStatus.COMPLETED

    def add_metadata(self, key: str, value: str) -> None:
        self.metadata[key] = value
