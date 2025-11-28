from __future__ import annotations
from dataclasses import dataclass

from .enums import SecurityLevel


@dataclass
class AccessBadge:
    badge_id: str
    owner_id: str
    level: SecurityLevel
    revoked: bool = False

    def upgrade(self, new_level: SecurityLevel) -> None:
        self.level = new_level

    def revoke(self) -> None:
        self.revoked = True

    def is_active(self) -> bool:
        return not self.revoked


@dataclass
class SecurityCheckpoint:
    checkpoint_id: str
    required_level: SecurityLevel
    name: str = ""

    def can_pass(self, badge: AccessBadge) -> bool:
        if badge.revoked:
            return False
        return badge.level.value >= self.required_level.value

    def describe(self) -> str:
        return f"{self.checkpoint_id} ({self.name}) requires {self.required_level.name}"
