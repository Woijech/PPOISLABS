"""Core abstractions and protocols for documentflow system."""

from .base import BaseEntity, IdentifiableMixin, TimestampMixin
from .protocols import (
    Validatable,
    Approvable,
    Signable,
    Storable,
    NotifierProtocol,
    PaymentProcessorProtocol,
    DocumentLike,
    DocumentRepositoryProtocol,
)

__all__ = [
    "BaseEntity",
    "IdentifiableMixin",
    "TimestampMixin",
    "Validatable",
    "Approvable",
    "Signable",
    "Storable",
    "NotifierProtocol",
    "PaymentProcessorProtocol",
    "DocumentLike",
    "DocumentRepositoryProtocol",
]
