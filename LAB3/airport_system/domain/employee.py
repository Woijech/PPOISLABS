from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .enums import EmployeeRole


@dataclass
class Employee:
    employee_id: str
    name: str
    role: EmployeeRole
    active: bool = True
    username: str = ""
    password_hash: str = ""

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def can_access_high_security(self) -> bool:
        return self.role in {EmployeeRole.PILOT, EmployeeRole.SECURITY}

    def set_password(self, raw_password: str) -> None:
        self.password_hash = raw_password[::-1]

    def verify_password(self, raw_password: str) -> bool:
        return self.password_hash == raw_password[::-1]

    def is_active_staff(self) -> bool:
        return self.active


@dataclass
class Pilot(Employee):
    license_number: str = ""
    flight_hours: int = 0

    def add_flight_hours(self, hours: int) -> None:
        if hours <= 0:
            raise ValueError("Hours must be positive")
        self.flight_hours += hours


@dataclass
class CabinCrew(Employee):
    languages_spoken: int = 1

    def can_serve_language(self, required_count: int) -> bool:
        return self.languages_spoken >= required_count


@dataclass
class GroundStaff(Employee):
    station: Optional[str] = None

    def assign_station(self, station: str) -> None:
        self.station = station

    def is_assigned(self) -> bool:
        return self.station is not None
