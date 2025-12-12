from .base import AirportError


class AccessDeniedError(AirportError):
    pass


class InvalidBadgeError(AirportError):
    pass
