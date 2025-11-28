"""Extended tests for SecurityCheckpoint and AccessBadge models."""
from airport_system.domain.security import AccessBadge, SecurityCheckpoint
from airport_system.domain.enums import SecurityLevel


class TestAccessBadgeExtended:
    """Extended tests for AccessBadge."""

    def test_badge_is_active_true(self):
        """Test is_active for active badge."""
        badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.STAFF)
        assert badge.is_active() is True

    def test_badge_is_active_false(self):
        """Test is_active for revoked badge."""
        badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.STAFF)
        badge.revoke()
        assert badge.is_active() is False

    def test_badge_upgrade(self):
        """Test upgrading badge level."""
        badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.STAFF)
        badge.upgrade(SecurityLevel.RESTRICTED)
        assert badge.level == SecurityLevel.RESTRICTED


class TestSecurityCheckpointExtended:
    """Extended tests for SecurityCheckpoint."""

    def test_checkpoint_describe(self):
        """Test describe method."""
        checkpoint = SecurityCheckpoint(
            checkpoint_id="C1",
            required_level=SecurityLevel.STAFF,
            name="Staff Only Area"
        )
        desc = checkpoint.describe()
        assert "C1" in desc
        assert "Staff Only Area" in desc
        assert "STAFF" in desc

    def test_checkpoint_can_pass_by_level(self):
        """Test can_pass with different badge levels."""
        checkpoint = SecurityCheckpoint(
            checkpoint_id="C1",
            required_level=SecurityLevel.STAFF,
            name="Staff Checkpoint"
        )
        
        # Public level badge should fail
        public_badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.PUBLIC)
        assert checkpoint.can_pass(public_badge) is False
        
        # Staff level badge should pass
        staff_badge = AccessBadge(badge_id="B2", owner_id="E2", level=SecurityLevel.STAFF)
        assert checkpoint.can_pass(staff_badge) is True
        
        # Restricted level badge should pass (higher level)
        restricted_badge = AccessBadge(badge_id="B3", owner_id="E3", level=SecurityLevel.RESTRICTED)
        assert checkpoint.can_pass(restricted_badge) is True
