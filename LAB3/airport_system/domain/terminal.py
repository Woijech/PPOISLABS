from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .enums import SecurityLevel


@dataclass
class Gate:
    gate_id: str
    terminal_code: str
    is_open: bool = True
    current_flight_id: Optional[str] = None
    supports_international: bool = False

    def assign_flight(self, flight_id: str) -> None:
        self.current_flight_id = flight_id

    def clear_flight(self) -> None:
        self.current_flight_id = None

    def close(self) -> None:
        self.is_open = False

    def open(self) -> None:
        self.is_open = True

    def is_free(self) -> bool:
        return self.is_open and self.current_flight_id is None


@dataclass
class Terminal:
    code: str
    gates: List[Gate] = field(default_factory=list)
    name: str = ""
    security_level: SecurityLevel = SecurityLevel.PUBLIC

    def add_gate(self, gate: Gate) -> None:
        self.gates.append(gate)

    def find_free_gate(self) -> Optional[Gate]:
        for gate in self.gates:
            if gate.is_free():
                return gate
        return None

    def is_international_terminal(self) -> bool:
        return any(g.supports_international for g in self.gates)

    def available_gates_count(self) -> int:
        return sum(1 for g in self.gates if g.is_free())


@dataclass
class BoardingPass:
    boarding_pass_id: str
    booking_id: str
    passenger_name: str
    gate_id: str
    seat_number: str

    def change_gate(self, new_gate_id: str) -> None:
        self.gate_id = new_gate_id
