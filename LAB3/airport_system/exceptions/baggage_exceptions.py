from .base import AirportError


class BaggageNotFoundError(AirportError):
    pass


class OverweightBaggageError(AirportError):
    pass
