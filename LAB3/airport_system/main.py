"""
Simple entry point demonstrating basic usage of the airport system.
"""
from datetime import datetime, timedelta

from .config import AppConfig
from .domain.aircraft import Aircraft, Seat
from .domain.enums import FlightStatus, SeatClass
from .domain.flight import Flight
from .repositories.flight_repository import FlightRepository
from .services.flight_service import FlightService


def main() -> None:
    config = AppConfig.default()
    print(f"Starting Airport System for {config.airport_name} (baggage limit {config.baggage_limit_kg()} kg)")

    repo = FlightRepository()
    service = FlightService(flights=repo)

    aircraft = Aircraft(registration="N100AB", model="A320", manufacturer="Airbus", range_km=6100)
    aircraft.add_seat(Seat("1A", SeatClass.FIRST, is_exit_row=False))
    now = datetime.now()
    flight = Flight(
        flight_id="AB123",
        origin="SFO",
        destination="LAX",
        departure_time=now + timedelta(hours=2),
        arrival_time=now + timedelta(hours=4),
        aircraft=aircraft,
        distance_km=550,
    )
    service.schedule_flight(flight)
    service.update_status("AB123", FlightStatus.BOARDING)
    print("Scheduled flights:", [f.flight_id for f in service.upcoming_flights(datetime.now())])


if __name__ == "__main__":
    main()
