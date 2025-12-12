"""Extended tests for BaggageService."""
import pytest

from airport_system.domain.enums import BaggageStatus
from airport_system.services.baggage_service import BaggageService
from airport_system.exceptions import BaggageNotFoundError


class TestBaggageServiceExtended:
    """Extended tests for BaggageService."""

    def test_mark_lost(self):
        """Test marking baggage as lost."""
        service = BaggageService(max_weight_kg=32.0)
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
        item = service.mark_lost("TAG1")
        assert item.status == BaggageStatus.LOST

    def test_mark_lost_not_found(self):
        """Test marking non-existent baggage as lost."""
        service = BaggageService(max_weight_kg=32.0)
        with pytest.raises(BaggageNotFoundError):
            service.mark_lost("NONEXISTENT")

    def test_count_by_status(self):
        """Test counting baggage by status."""
        service = BaggageService(max_weight_kg=32.0)
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
        service.check_in_baggage("TAG2", "BKG1", 15.0, "SFO")
        service.check_in_baggage("TAG3", "BKG2", 10.0, "SFO")
        service.load_to_aircraft("TAG1", "BELT")
        
        checked_in_count = service.count_by_status(BaggageStatus.CHECKED_IN)
        loaded_count = service.count_by_status(BaggageStatus.LOADED)
        
        assert checked_in_count == 2
        assert loaded_count == 1

    def test_total_weight(self):
        """Test calculating total weight of all baggage."""
        service = BaggageService(max_weight_kg=32.0)
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
        service.check_in_baggage("TAG2", "BKG1", 15.0, "SFO")
        service.check_in_baggage("TAG3", "BKG2", 10.5, "SFO")
        
        total = service.total_weight()
        assert total == 45.5

    def test_find_by_booking(self):
        """Test finding baggage by booking ID."""
        service = BaggageService(max_weight_kg=32.0)
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
        service.check_in_baggage("TAG2", "BKG1", 15.0, "SFO")
        service.check_in_baggage("TAG3", "BKG2", 10.0, "SFO")
        
        items = service.find_by_booking("BKG1")
        assert len(items) == 2
        assert all(item.tag.booking_id == "BKG1" for item in items)

    def test_find_by_booking_none(self):
        """Test finding baggage by booking ID when none exist."""
        service = BaggageService(max_weight_kg=32.0)
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
        
        items = service.find_by_booking("NONEXISTENT")
        assert items == []
