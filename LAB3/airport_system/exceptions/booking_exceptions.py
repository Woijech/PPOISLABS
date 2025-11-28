from .base import AirportError


class BookingNotFoundError(AirportError):
    pass


class BookingAlreadyPaidError(AirportError):
    pass


class SeatUnavailableError(AirportError):
    pass
