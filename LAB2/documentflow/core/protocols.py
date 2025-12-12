"""Protocols and abstract base classes for documentflow system."""

from __future__ import annotations
from abc import ABC
from typing import Protocol, runtime_checkable, Optional, Iterable


class Validatable(ABC):
    """Protocol for entities that can be validated."""
    
    def validate(self) -> None:
        """Validate the entity state."""
        ...


class Approvable(ABC):
    """Protocol for entities that can be approved."""
    
    def approve(self) -> None:
        """Approve this entity."""
        ...


class Signable(ABC):
    """Protocol for entities that can be digitally signed."""
    
    def sign(self, user_id: str) -> None:
        """Sign this entity with user's digital signature."""
        ...


class Storable(ABC):
    """Protocol for entities that can be stored."""
    
    def store(self) -> str:
        """Store this entity and return storage identifier."""
        ...


@runtime_checkable
class NotifierProtocol(Protocol):
    """Protocol for notification services."""
    
    def notify(self, message: str) -> None:
        """Send a notification with the given message."""
        ...


@runtime_checkable
class PaymentProcessorProtocol(Protocol):
    """Protocol for payment processing services."""
    
    def transfer(self, src_account: str, dst_account: str, amount: int) -> str:
        """Transfer money between accounts and return transaction ID."""
        ...


class DocumentLike(Protocol):
    """Protocol defining the interface for document-like objects."""
    
    number: str
    title: str

    def validate(self) -> None:
        """Validate the document."""
        ...


@runtime_checkable
class DocumentRepositoryProtocol(Protocol):
    """Protocol for document repository implementations."""
    
    def save(self, doc: "DocumentLike") -> None:
        """Save a document to the repository."""
        ...

    def get(self, number: str) -> Optional["DocumentLike"]:
        """Retrieve a document by its number."""
        ...

    def exists(self, number: str) -> bool:
        """Check if a document exists in the repository."""
        ...

    def search(self, query: str) -> Iterable["DocumentLike"]:
        """Search for documents matching the query."""
        ...
