from __future__ import annotations
from dataclasses import dataclass
from typing import List

from ..domain.enums import PaymentStatus
from ..domain.payment import CardPayment, Money, Payment
from ..exceptions import CurrencyMismatchError, InsufficientFundsError, PaymentDeclinedError
from ..utils import id_generator


@dataclass
class PaymentService:
    currency: str = "USD"

    def charge_card(self, booking_id: str, amount: Money, card: CardPayment) -> Payment:
        if amount.currency != self.currency:
            raise CurrencyMismatchError("Unsupported currency")
        if amount.amount <= 0:
            raise InsufficientFundsError("Amount must be positive")
        payment_id = id_generator.next_id("PAY")
        payment = Payment(payment_id=payment_id, booking_id=booking_id, amount=amount)
        authorised = card.authorize(amount)
        if not authorised:
            payment.mark_declined()
            raise PaymentDeclinedError("Card authorisation failed")
        payment.mark_completed()
        return payment

    def refund_payment(self, payment: Payment) -> Payment:
        if payment.status != PaymentStatus.COMPLETED:
            raise PaymentDeclinedError("Only completed payments can be refunded")
        payment.mark_refunded()
        return payment

    def split_payment(self, booking_id: str, total: Money, parts: int, card: CardPayment) -> List[Payment]:
        share_amount = total.allocate(parts)
        payments: List[Payment] = []
        for _ in range(parts):
            share = Money(amount=share_amount, currency=total.currency, precision=total.precision)
            payments.append(self.charge_card(booking_id, share, card))
        return payments

    def transfer_between_cards(self, from_card: CardPayment, to_card: CardPayment, amount: Money) -> bool:
        # учебный пример перевода денег: авторизуем списание и "зачисление"
        if amount.currency != self.currency:
            raise CurrencyMismatchError("Unsupported currency")
        if not from_card.authorize(amount):
            raise PaymentDeclinedError("Source card authorisation failed")
        # для учебных целей зачисление всегда успешно
        return True
