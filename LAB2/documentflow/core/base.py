"""Base classes for documentflow entities."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity:
    """Base entity with timestamp tracking."""
    
    created_at: datetime = field(default_factory=datetime.utcnow, init=False)
    updated_at: datetime = field(default_factory=datetime.utcnow, init=False)

    def touch(self) -> None:
        """Update the modified timestamp."""
        self.updated_at = datetime.utcnow()


class IdentifiableMixin:
    """Mixin for entities with unique identifiers."""
    
    id: str

    def identity(self) -> str:
        """Return the unique identifier of this entity."""
        return self.id


class TimestampMixin:
    """Mixin for entities with creation and update timestamps."""
    
    created_at: datetime
    updated_at: datetime
