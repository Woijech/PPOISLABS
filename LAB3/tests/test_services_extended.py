"""Extended tests for FlightService and BookingService."""
import pytest
from datetime import datetime, timedelta

from airport_system.domain.aircraft import Aircraft
from airport_system.domain.flight import Flight
from airport_system.domain.enums import FlightStatus, BookingStatus
from airport_system.repositories.flight_repository import FlightRepository
from airport_system.repositories.booking_repository import BookingRepository
from airport_system.services.flight_service import FlightService
from airport_system.services.booking_service import BookingService
from airport_system.exceptions import FlightNotFoundError, FlightAlreadyDepartedError, BookingNotFoundError


def _create_flight(flight_id: str) -> Flight:
    """Helper to create a flight."""
    aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
    now = datetime.now()
    return Flight(
        flight_id=flight_id,
        origin="SFO",
        destination="LAX",
        departure_time=now + timedelta(hours=2),
        arrival_time=now + timedelta(hours=4),
        aircraft=aircraft,
        distance_km=500
    )


class TestFlightServiceExtended:
    """Extended tests for FlightService."""

    def test_schedule_flight_duplicate(self):
        """Test scheduling duplicate flight raises error."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        flight = _create_flight("FL1")
        service.schedule_flight(flight)
        
        with pytest.raises(ValueError, match="Flight already exists"):
            service.schedule_flight(flight)

    def test_update_status_not_found(self):
        """Test updating status of non-existent flight."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        
        with pytest.raises(FlightNotFoundError):
            service.update_status("NONEXISTENT", FlightStatus.BOARDING)

    def test_update_status_departed_invalid(self):
        """Test cannot change departed flight to non-arrived status."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        flight = _create_flight("FL1")
        service.schedule_flight(flight)
        service.update_status("FL1", FlightStatus.DEPARTED)
        
        with pytest.raises(FlightAlreadyDepartedError):
            service.update_status("FL1", FlightStatus.BOARDING)

    def test_update_status_departed_to_arrived(self):
        """Test can change departed flight to arrived."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        flight = _create_flight("FL1")
        service.schedule_flight(flight)
        service.update_status("FL1", FlightStatus.DEPARTED)
        result = service.update_status("FL1", FlightStatus.ARRIVED)
        assert result.status == FlightStatus.ARRIVED

    def test_cancel_flight_success(self):
        """Test canceling flight."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        flight = _create_flight("FL1")
        service.schedule_flight(flight)
        
        cancelled = service.cancel_flight("FL1")
        assert cancelled.status == FlightStatus.CANCELLED

    def test_cancel_flight_not_found(self):
        """Test canceling non-existent flight."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        
        with pytest.raises(FlightNotFoundError):
            service.cancel_flight("NONEXISTENT")

    def test_find_by_route(self):
        """Test finding flights by route."""
        repo = FlightRepository()
        service = FlightService(flights=repo)
        
        # Add some flights
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
        now = datetime.now()
        
        flight1 = Flight(
            flight_id="FL1", origin="SFO", destination="LAX",
            departure_time=now + timedelta(hours=2),
            arrival_time=now + timedelta(hours=4),
            aircraft=aircraft, distance_km=500
        )
        flight2 = Flight(
            flight_id="FL2", origin="SFO", destination="LAX",
            departure_time=now + timedelta(hours=5),
            arrival_time=now + timedelta(hours=7),
            aircraft=aircraft, distance_km=500
        )
        flight3 = Flight(
            flight_id="FL3", origin="JFK", destination="SFO",
            departure_time=now + timedelta(hours=2),
            arrival_time=now + timedelta(hours=8),
            aircraft=aircraft, distance_km=4000
        )
        
        service.schedule_flight(flight1)
        service.schedule_flight(flight2)
        service.schedule_flight(flight3)
        
        flights = service.find_by_route("SFO", "LAX")
        assert len(flights) == 2
        assert all(f.origin == "SFO" and f.destination == "LAX" for f in flights)


class TestBookingServiceExtended:
    """Extended tests for BookingService."""

    def test_confirm_booking_not_found(self):
        """Test confirming non-existent booking."""
        repo = BookingRepository()
        service = BookingService(bookings=repo)
        
        with pytest.raises(BookingNotFoundError):
            service.confirm_booking("NONEXISTENT")

    def test_cancel_booking_not_found(self):
        """Test canceling non-existent booking."""
        repo = BookingRepository()
        service = BookingService(bookings=repo)
        
        with pytest.raises(BookingNotFoundError):
            service.cancel_booking("NONEXISTENT")
