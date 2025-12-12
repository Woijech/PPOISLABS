from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List

from ..domain.enums import FlightStatus
from ..domain.flight import Flight
from ..exceptions import FlightAlreadyDepartedError, FlightNotFoundError
from ..repositories.flight_repository import FlightRepository


@dataclass
class FlightService:
    flights: FlightRepository

    def schedule_flight(self, flight: Flight) -> None:
        if self.flights.get(flight.flight_id):
            raise ValueError("Flight already exists")
        self.flights.add(flight.flight_id, flight)

    def update_status(self, flight_id: str, status: FlightStatus) -> Flight:
        flight = self.flights.get(flight_id)
        if not flight:
            raise FlightNotFoundError(f"Flight {flight_id} not found")
        if flight.status == FlightStatus.DEPARTED and status != FlightStatus.ARRIVED:
            raise FlightAlreadyDepartedError("Cannot change status of departed flight")
        flight.status = status
        return flight

    def upcoming_flights(self, now: datetime) -> List[Flight]:
        return self.flights.find_active(now)

    def cancel_flight(self, flight_id: str) -> Flight:
        flight = self.flights.get(flight_id)
        if not flight:
            raise FlightNotFoundError(f"Flight {flight_id} not found")
        flight.status = FlightStatus.CANCELLED
        return flight

    def find_by_route(self, origin: str, destination: str) -> List[Flight]:
        return self.flights.find_by_route(origin, destination)
