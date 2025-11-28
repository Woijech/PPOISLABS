from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

from ..domain.baggage import BaggageItem, BaggageTag
from ..domain.enums import BaggageStatus
from ..exceptions import BaggageNotFoundError, OverweightBaggageError


@dataclass
class BaggageService:
    max_weight_kg: float = 32.0
    _items: Dict[str, BaggageItem] = field(default_factory=dict)

    def check_in_baggage(self, tag_id: str, booking_id: str, weight_kg: float, location: str) -> BaggageItem:
        if weight_kg > self.max_weight_kg:
            raise OverweightBaggageError("Baggage overweight")
        tag = BaggageTag(tag_id=tag_id, booking_id=booking_id)
        item = BaggageItem(tag=tag, weight_kg=weight_kg)
        item.check_in(location)
        self._items[tag_id] = item
        return item

    def load_to_aircraft(self, tag_id: str, location: str) -> BaggageItem:
        item = self._items.get(tag_id)
        if not item:
            raise BaggageNotFoundError(f"Baggage with tag {tag_id} not found")
        item.mark_loaded(location)
        return item

    def mark_lost(self, tag_id: str) -> BaggageItem:
        item = self._items.get(tag_id)
        if not item:
            raise BaggageNotFoundError(f"Baggage with tag {tag_id} not found")
        item.mark_lost()
        return item

    def count_by_status(self, status: BaggageStatus) -> int:
        return sum(1 for item in self._items.values() if item.status == status)

    def total_weight(self) -> float:
        return sum(item.weight_kg for item in self._items.values())

    def find_by_booking(self, booking_id: str) -> List[BaggageItem]:
        return [item for item in self._items.values() if item.tag.booking_id == booking_id]
