"""
Custom exceptions for the Airport System.
"""
from .base import AirportError
from .booking_exceptions import (
    BookingNotFoundError,
    BookingAlreadyPaidError,
    SeatUnavailableError,
)
from .payment_exceptions import (
    PaymentDeclinedError,
    InsufficientFundsError,
    CurrencyMismatchError,
)
from .security_exceptions import AccessDeniedError, InvalidBadgeError
from .baggage_exceptions import BaggageNotFoundError, OverweightBaggageError
from .flight_exceptions import FlightNotFoundError, FlightAlreadyDepartedError

__all__ = [
    "AirportError",
    "BookingNotFoundError",
    "BookingAlreadyPaidError",
    "SeatUnavailableError",
    "PaymentDeclinedError",
    "InsufficientFundsError",
    "CurrencyMismatchError",
    "AccessDeniedError",
    "InvalidBadgeError",
    "BaggageNotFoundError",
    "OverweightBaggageError",
    "FlightNotFoundError",
    "FlightAlreadyDepartedError",
]
