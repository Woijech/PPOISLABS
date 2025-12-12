from __future__ import annotations
from typing import List

from .base import InMemoryRepository
from ..domain.booking import Booking
from ..exceptions import BookingNotFoundError


class BookingRepository(InMemoryRepository[Booking]):
    def find_by_passenger(self, passenger_id: str) -> List[Booking]:
        return [b for b in self.all() if b.passenger_id == passenger_id]

    def get_required(self, booking_id: str) -> Booking:
        booking = self.get(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking {booking_id} not found")
        return booking
