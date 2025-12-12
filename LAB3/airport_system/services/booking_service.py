from __future__ import annotations
from dataclasses import dataclass
from typing import List

from ..domain.booking import Booking
from ..domain.enums import BookingStatus
from ..exceptions import BookingAlreadyPaidError, BookingNotFoundError
from ..repositories.booking_repository import BookingRepository
from ..utils import id_generator


@dataclass
class BookingService:
    bookings: BookingRepository

    def create_booking(self, passenger_id: str, flight_id: str) -> Booking:
        booking_id = id_generator.next_id("BKG")
        booking = Booking(booking_id=booking_id, passenger_id=passenger_id, flight_id=flight_id)
        self.bookings.add(booking_id, booking)
        return booking

    def confirm_booking(self, booking_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking {booking_id} not found")
        booking.confirm()
        return booking

    def mark_paid(self, booking_id: str, payment_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking {booking_id} not found")
        if booking.status in (BookingStatus.CANCELLED, BookingStatus.COMPLETED):
            raise BookingAlreadyPaidError("Cannot pay for finalised booking")
        booking.add_payment(payment_id)
        booking.status = BookingStatus.COMPLETED
        booking.touch()
        return booking

    def cancel_booking(self, booking_id: str) -> Booking:
        booking = self.bookings.get(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking {booking_id} not found")
        booking.cancel()
        return booking

    def get_bookings_for_passenger(self, passenger_id: str) -> List[Booking]:
        return self.bookings.find_by_passenger(passenger_id)
