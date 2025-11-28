from __future__ import annotations
from dataclasses import dataclass

from ..domain.security import AccessBadge, SecurityCheckpoint
from ..exceptions import AccessDeniedError, InvalidBadgeError


@dataclass
class SecurityService:
    def pass_checkpoint(self, badge: AccessBadge, checkpoint: SecurityCheckpoint) -> None:
        if not badge.badge_id:
            raise InvalidBadgeError("Badge has no id")
        if not checkpoint.can_pass(badge):
            raise AccessDeniedError("Access denied")

    def upgrade_badge(self, badge: AccessBadge, new_level) -> AccessBadge:
        badge.upgrade(new_level)
        return badge
