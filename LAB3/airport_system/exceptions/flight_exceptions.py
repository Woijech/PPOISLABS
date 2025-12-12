from .base import AirportError


class FlightNotFoundError(AirportError):
    pass


class FlightAlreadyDepartedError(AirportError):
    pass
