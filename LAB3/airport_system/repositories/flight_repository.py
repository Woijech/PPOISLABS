from __future__ import annotations
from datetime import datetime
from typing import List

from .base import InMemoryRepository
from ..domain.flight import Flight


class FlightRepository(InMemoryRepository[Flight]):
    def find_active(self, now: datetime) -> List[Flight]:
        return [f for f in self.all() if f.departure_time >= now]

    def find_by_route(self, origin: str, destination: str) -> List[Flight]:
        return [f for f in self.all() if f.origin == origin and f.destination == destination]
