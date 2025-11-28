from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from .enums import BookingStatus


@dataclass
class Booking:
    booking_id: str
    passenger_id: str
    flight_id: str
    status: BookingStatus = BookingStatus.CREATED
    ticket_ids: List[str] = field(default_factory=list)
    payment_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    refundable: bool = False

    def confirm(self) -> None:
        if self.status != BookingStatus.CREATED:
            raise ValueError("Only newly created bookings can be confirmed")
        self.status = BookingStatus.CONFIRMED
        self.touch()

    def cancel(self) -> None:
        if self.status in (BookingStatus.CANCELLED, BookingStatus.COMPLETED):
            raise ValueError("Booking already finalized")
        self.status = BookingStatus.CANCELLED
        self.touch()

    def add_ticket(self, ticket_id: str) -> None:
        if ticket_id not in self.ticket_ids:
            self.ticket_ids.append(ticket_id)
            self.touch()

    def add_payment(self, payment_id: str) -> None:
        if payment_id not in self.payment_ids:
            self.payment_ids.append(payment_id)
            self.touch()

    def mark_checked_in(self) -> None:
        self.status = BookingStatus.CHECKED_IN
        self.touch()

    def is_refundable(self) -> bool:
        return self.refundable and self.status in (BookingStatus.CONFIRMED, BookingStatus.CREATED)

    def has_payments(self) -> bool:
        return bool(self.payment_ids)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
