from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from .aircraft import Aircraft
from .enums import FlightStatus


@dataclass
class Flight:
    flight_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    aircraft: Aircraft
    status: FlightStatus = FlightStatus.SCHEDULED
    gate_id: Optional[str] = None
    terminal_code: Optional[str] = None
    distance_km: int = 0

    def delay(self, minutes: int) -> None:
        if minutes <= 0:
            raise ValueError("Delay minutes must be positive")
        delta = timedelta(minutes=minutes)
        self.departure_time = self.departure_time + delta
        self.arrival_time = self.arrival_time + delta
        self.status = FlightStatus.DELAYED

    def depart(self) -> None:
        self.status = FlightStatus.DEPARTED

    def arrive(self) -> None:
        self.status = FlightStatus.ARRIVED

    def assign_gate(self, gate_id: str, terminal_code: str) -> None:
        self.gate_id = gate_id
        self.terminal_code = terminal_code

    def flight_duration_hours(self) -> float:
        delta = self.arrival_time - self.departure_time
        return round(delta.total_seconds() / 3600.0, 2)
