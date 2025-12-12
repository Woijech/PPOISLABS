from airport_system.domain.enums import SecurityLevel
from airport_system.domain.security import AccessBadge, SecurityCheckpoint
from airport_system.exceptions import AccessDeniedError, InvalidBadgeError
from airport_system.services.security_service import SecurityService


def test_security_pass_and_fail():
    service = SecurityService()
    badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.STAFF)
    checkpoint = SecurityCheckpoint(checkpoint_id="C1", required_level=SecurityLevel.PUBLIC)
    service.pass_checkpoint(badge, checkpoint)

    badge_low = AccessBadge(badge_id="B2", owner_id="E2", level=SecurityLevel.PUBLIC)
    strict = SecurityCheckpoint(checkpoint_id="C2", required_level=SecurityLevel.STAFF)
    try:
        service.pass_checkpoint(badge_low, strict)
    except AccessDeniedError:
        pass
    else:
        assert False

def test_invalid_badge_raises():
    service = SecurityService()
    badge = AccessBadge(badge_id="", owner_id="E1", level=SecurityLevel.STAFF)
    checkpoint = SecurityCheckpoint(checkpoint_id="C1", required_level=SecurityLevel.PUBLIC)
    try:
        service.pass_checkpoint(badge, checkpoint)
    except InvalidBadgeError:
        pass
    else:
        assert False

def test_upgrade_badge():
    service = SecurityService()
    badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.PUBLIC)
    upgraded = service.upgrade_badge(badge, SecurityLevel.STAFF)
    assert upgraded.level == SecurityLevel.STAFF
