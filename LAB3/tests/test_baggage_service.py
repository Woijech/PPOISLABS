from airport_system.domain.enums import BaggageStatus
from airport_system.exceptions import BaggageNotFoundError, OverweightBaggageError
from airport_system.services.baggage_service import BaggageService


def test_check_in_and_load_baggage():
    service = BaggageService(max_weight_kg=32)
    item = service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
    assert item.status == BaggageStatus.CHECKED_IN

    loaded = service.load_to_aircraft("TAG1", "SFO-BELT")
    assert loaded.status == BaggageStatus.LOADED
    assert service.count_by_status(BaggageStatus.LOADED) == 1

def test_overweight_baggage_raises():
    service = BaggageService(max_weight_kg=10)
    try:
        service.check_in_baggage("TAG1", "BKG1", 20.0, "SFO")
    except OverweightBaggageError:
        pass
    else:
        assert False

def test_missing_baggage_raises():
    service = BaggageService()
    try:
        service.load_to_aircraft("UNKNOWN", "SFO")
    except BaggageNotFoundError:
        pass
    else:
        assert False

def test_total_weight_and_find_by_booking():
    service = BaggageService()
    service.check_in_baggage("TAG1", "BKG1", 10.0, "SFO")
    service.check_in_baggage("TAG2", "BKG1", 15.0, "SFO")
    assert service.total_weight() == 25.0
    items = service.find_by_booking("BKG1")
    assert len(items) == 2
