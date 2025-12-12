from .base import AirportError


class PaymentDeclinedError(AirportError):
    pass


class InsufficientFundsError(AirportError):
    pass


class CurrencyMismatchError(AirportError):
    pass
