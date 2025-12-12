from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from .flight import Flight


@dataclass
class DailySchedule:
    day: date
    flights: List[Flight] = field(default_factory=list)
    notes: str = ""

    def add_flight(self, flight: Flight) -> None:
        self.flights.append(flight)

    def flights_from(self, origin: str) -> List[Flight]:
        return [f for f in self.flights if f.origin == origin]

    def flights_to(self, destination: str) -> List[Flight]:
        return [f for f in self.flights if f.destination == destination]


@dataclass
class AirportSchedule:
    days: Dict[date, DailySchedule] = field(default_factory=dict)

    def add_flight(self, flight: Flight) -> None:
        day = flight.departure_time.date()
        if day not in self.days:
            self.days[day] = DailySchedule(day)
        self.days[day].add_flight(flight)

    def flights_on(self, day: date) -> List[Flight]:
        schedule = self.days.get(day)
        return schedule.flights if schedule else []

    def total_flights(self) -> int:
        return sum(len(d.flights) for d in self.days.values())

    def remove_flight(self, flight_id: str) -> None:
        for schedule in self.days.values():
            schedule.flights = [f for f in schedule.flights if f.flight_id != flight_id]
