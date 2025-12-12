from __future__ import annotations
from enum import Enum, auto


class FlightStatus(Enum):
    SCHEDULED = auto()
    BOARDING = auto()
    DEPARTED = auto()
    ARRIVED = auto()
    CANCELLED = auto()
    DELAYED = auto()


class BaggageStatus(Enum):
    CREATED = auto()
    CHECKED_IN = auto()
    LOADED = auto()
    UNLOADED = auto()
    LOST = auto()
    DELIVERED = auto()


class PaymentStatus(Enum):
    PENDING = auto()
    COMPLETED = auto()
    DECLINED = auto()
    REFUNDED = auto()


class BookingStatus(Enum):
    CREATED = auto()
    CONFIRMED = auto()
    CANCELLED = auto()
    CHECKED_IN = auto()
    COMPLETED = auto()


class SeatClass(Enum):
    ECONOMY = auto()
    PREMIUM_ECONOMY = auto()
    BUSINESS = auto()
    FIRST = auto()


class EmployeeRole(Enum):
    PILOT = auto()
    CABIN_CREW = auto()
    GROUND_STAFF = auto()
    SECURITY = auto()


class SecurityLevel(Enum):
    PUBLIC = auto()
    STAFF = auto()
    RESTRICTED = auto()
    HIGH_SECURITY = auto()
