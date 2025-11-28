from datetime import datetime, timedelta

from airport_system.domain.aircraft import Aircraft, Seat
from airport_system.domain.enums import FlightStatus, SeatClass
from airport_system.domain.flight import Flight
from airport_system.exceptions import FlightAlreadyDepartedError, FlightNotFoundError
from airport_system.repositories.flight_repository import FlightRepository
from airport_system.services.flight_service import FlightService


def create_flight(flight_id: str) -> Flight:
    aircraft = Aircraft(registration="REG1", model="A320", manufacturer="Airbus", range_km=6100, seats=[Seat("1A", SeatClass.FIRST)])
    now = datetime.now()
    return Flight(
        flight_id=flight_id,
        origin="SFO",
        destination="LAX",
        departure_time=now + timedelta(hours=1),
        arrival_time=now + timedelta(hours=3),
        aircraft=aircraft,
        distance_km=550,
    )


def test_schedule_and_update_status():
    repo = FlightRepository()
    service = FlightService(flights=repo)
    flight = create_flight("FL1")
    service.schedule_flight(flight)
    updated = service.update_status("FL1", FlightStatus.BOARDING)
    assert updated.status == FlightStatus.BOARDING

def test_update_missing_flight_raises():
    repo = FlightRepository()
    service = FlightService(flights=repo)
    try:
        service.update_status("UNKNOWN", FlightStatus.BOARDING)
    except FlightNotFoundError:
        pass
    else:
        assert False

def test_update_departed_flight_raises():
    repo = FlightRepository()
    service = FlightService(flights=repo)
    flight = create_flight("FL2")
    service.schedule_flight(flight)
    flight.status = FlightStatus.DEPARTED
    try:
        service.update_status("FL2", FlightStatus.CANCELLED)
    except FlightAlreadyDepartedError:
        pass
    else:
        assert False

def test_upcoming_and_cancel_and_find_by_route():
    repo = FlightRepository()
    service = FlightService(flights=repo)
    flight = create_flight("FL3")
    service.schedule_flight(flight)
    upcoming = service.upcoming_flights(datetime.now())
    assert any(f.flight_id == "FL3" for f in upcoming)

    cancelled = service.cancel_flight("FL3")
    assert cancelled.status == FlightStatus.CANCELLED

    by_route = service.find_by_route("SFO", "LAX")
    assert any(f.flight_id == "FL3" for f in by_route)
