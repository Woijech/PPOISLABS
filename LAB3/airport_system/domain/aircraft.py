from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from .enums import SeatClass


@dataclass
class Seat:
    seat_number: str
    seat_class: SeatClass
    is_available: bool = True
    is_exit_row: bool = False

    def reserve(self) -> None:
        if not self.is_available:
            raise ValueError("Seat already reserved")
        self.is_available = False

    def release(self) -> None:
        self.is_available = True

    def is_premium(self) -> bool:
        return self.seat_class in {SeatClass.BUSINESS, SeatClass.FIRST}


@dataclass
class Aircraft:
    registration: str
    model: str
    seats: List[Seat] = field(default_factory=list)
    flight_hours: int = 0
    manufacturer: str = ""
    range_km: int = 0
    in_service: bool = True

    def add_seat(self, seat: Seat) -> None:
        self.seats.append(seat)

    def available_seats(self) -> List[Seat]:
        return [s for s in self.seats if s.is_available]

    def add_flight_hours(self, hours: int) -> None:
        if hours <= 0:
            raise ValueError("Hours must be positive")
        self.flight_hours += hours

    def retire(self) -> None:
        self.in_service = False

    def is_long_haul(self) -> bool:
        return self.range_km >= 6000
