from __future__ import annotations
from dataclasses import dataclass

from .enums import SeatClass


@dataclass
class Ticket:
    ticket_id: str
    passenger_id: str
    flight_id: str
    seat_number: str
    seat_class: SeatClass
    base_price: float
    checked_in: bool = False
    fare_basis: str = ""
    booking_class: str = ""
    refundable: bool = False

    def mark_checked_in(self) -> None:
        self.checked_in = True

    def calculate_price_with_tax(self, tax_rate: float) -> float:
        if tax_rate < 0:
            raise ValueError("Tax rate must be non-negative")
        return self.base_price * (1 + tax_rate)

    def is_upgradeable(self) -> bool:
        return self.seat_class in (SeatClass.ECONOMY, SeatClass.PREMIUM_ECONOMY)

    def can_refund(self) -> bool:
        return self.refundable and not self.checked_in
