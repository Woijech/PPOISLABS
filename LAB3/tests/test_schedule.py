"""Extended tests for DailySchedule and AirportSchedule models."""
from datetime import datetime, timedelta, date

from airport_system.domain.schedule import DailySchedule, AirportSchedule
from airport_system.domain.aircraft import Aircraft
from airport_system.domain.flight import Flight


def _create_flight(flight_id: str, origin: str, destination: str, dt: datetime) -> Flight:
    """Helper to create a flight."""
    aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
    return Flight(
        flight_id=flight_id,
        origin=origin,
        destination=destination,
        departure_time=dt,
        arrival_time=dt + timedelta(hours=2),
        aircraft=aircraft,
        distance_km=500
    )


class TestDailySchedule:
    """Tests for DailySchedule class."""

    def test_daily_schedule_basic(self):
        """Test basic DailySchedule creation."""
        today = date.today()
        schedule = DailySchedule(day=today, notes="Holiday schedule")
        assert schedule.day == today
        assert schedule.notes == "Holiday schedule"
        assert schedule.flights == []

    def test_daily_schedule_add_flight(self):
        """Test adding flight to daily schedule."""
        today = date.today()
        schedule = DailySchedule(day=today)
        now = datetime.now()
        flight = _create_flight("FL1", "SFO", "LAX", now)
        schedule.add_flight(flight)
        assert len(schedule.flights) == 1
        assert schedule.flights[0].flight_id == "FL1"

    def test_daily_schedule_flights_from(self):
        """Test filtering flights from origin."""
        today = date.today()
        schedule = DailySchedule(day=today)
        now = datetime.now()
        schedule.add_flight(_create_flight("FL1", "SFO", "LAX", now))
        schedule.add_flight(_create_flight("FL2", "SFO", "JFK", now))
        schedule.add_flight(_create_flight("FL3", "LAX", "SFO", now))
        
        flights_from_sfo = schedule.flights_from("SFO")
        assert len(flights_from_sfo) == 2
        assert all(f.origin == "SFO" for f in flights_from_sfo)

    def test_daily_schedule_flights_to(self):
        """Test filtering flights to destination."""
        today = date.today()
        schedule = DailySchedule(day=today)
        now = datetime.now()
        schedule.add_flight(_create_flight("FL1", "SFO", "LAX", now))
        schedule.add_flight(_create_flight("FL2", "JFK", "LAX", now))
        schedule.add_flight(_create_flight("FL3", "LAX", "SFO", now))
        
        flights_to_lax = schedule.flights_to("LAX")
        assert len(flights_to_lax) == 2
        assert all(f.destination == "LAX" for f in flights_to_lax)


class TestAirportSchedule:
    """Tests for AirportSchedule class."""

    def test_airport_schedule_basic(self):
        """Test basic AirportSchedule creation."""
        schedule = AirportSchedule()
        assert schedule.days == {}

    def test_airport_schedule_add_flight(self):
        """Test adding flight to airport schedule."""
        schedule = AirportSchedule()
        now = datetime.now()
        flight = _create_flight("FL1", "SFO", "LAX", now)
        schedule.add_flight(flight)
        
        flight_date = now.date()
        assert flight_date in schedule.days
        assert len(schedule.days[flight_date].flights) == 1

    def test_airport_schedule_add_multiple_flights_same_day(self):
        """Test adding multiple flights on same day."""
        schedule = AirportSchedule()
        now = datetime.now()
        flight1 = _create_flight("FL1", "SFO", "LAX", now)
        flight2 = _create_flight("FL2", "SFO", "JFK", now + timedelta(hours=1))
        schedule.add_flight(flight1)
        schedule.add_flight(flight2)
        
        assert schedule.total_flights() == 2

    def test_airport_schedule_flights_on(self):
        """Test getting flights on specific date."""
        schedule = AirportSchedule()
        now = datetime.now()
        flight = _create_flight("FL1", "SFO", "LAX", now)
        schedule.add_flight(flight)
        
        flights = schedule.flights_on(now.date())
        assert len(flights) == 1
        assert flights[0].flight_id == "FL1"

    def test_airport_schedule_flights_on_no_flights(self):
        """Test getting flights on date with no flights."""
        schedule = AirportSchedule()
        flights = schedule.flights_on(date.today())
        assert flights == []

    def test_airport_schedule_total_flights(self):
        """Test total flights count."""
        schedule = AirportSchedule()
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        
        schedule.add_flight(_create_flight("FL1", "SFO", "LAX", now))
        schedule.add_flight(_create_flight("FL2", "SFO", "JFK", now))
        schedule.add_flight(_create_flight("FL3", "LAX", "SFO", tomorrow))
        
        assert schedule.total_flights() == 3

    def test_airport_schedule_remove_flight(self):
        """Test removing flight from schedule."""
        schedule = AirportSchedule()
        now = datetime.now()
        schedule.add_flight(_create_flight("FL1", "SFO", "LAX", now))
        schedule.add_flight(_create_flight("FL2", "SFO", "JFK", now))
        
        assert schedule.total_flights() == 2
        schedule.remove_flight("FL1")
        assert schedule.total_flights() == 1
        
        flights = schedule.flights_on(now.date())
        assert all(f.flight_id != "FL1" for f in flights)

    def test_airport_schedule_remove_nonexistent_flight(self):
        """Test removing non-existent flight (should not raise)."""
        schedule = AirportSchedule()
        now = datetime.now()
        schedule.add_flight(_create_flight("FL1", "SFO", "LAX", now))
        
        # Should not raise
        schedule.remove_flight("NONEXISTENT")
        assert schedule.total_flights() == 1
