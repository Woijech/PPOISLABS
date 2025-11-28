from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .enums import BaggageStatus


@dataclass
class BaggageTag:
    tag_id: str
    booking_id: str
    priority: bool = False


@dataclass
class BaggageItem:
    tag: BaggageTag
    weight_kg: float
    status: BaggageStatus = BaggageStatus.CREATED
    location: Optional[str] = None
    length_cm: int = 0
    width_cm: int = 0
    height_cm: int = 0
    owner_id: str = ""

    def check_in(self, location: str) -> None:
        self.status = BaggageStatus.CHECKED_IN
        self.location = location

    def mark_loaded(self, location: str) -> None:
        self.status = BaggageStatus.LOADED
        self.location = location

    def mark_lost(self) -> None:
        self.status = BaggageStatus.LOST
        self.location = None

    def volume_liters(self) -> float:
        return round(self.length_cm * self.width_cm * self.height_cm / 1000.0, 2)

    def is_oversized(self, max_sum_cm: int) -> bool:
        return (self.length_cm + self.width_cm + self.height_cm) > max_sum_cm
