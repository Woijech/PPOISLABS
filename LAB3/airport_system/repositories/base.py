from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, Optional, TypeVar


T = TypeVar("T")


@dataclass
class InMemoryRepository(Generic[T]):
    _items: Dict[str, T] = field(default_factory=dict)

    def add(self, item_id: str, item: T) -> None:
        self._items[item_id] = item

    def get(self, item_id: str) -> Optional[T]:
        return self._items.get(item_id)

    def remove(self, item_id: str) -> None:
        self._items.pop(item_id, None)

    def all(self) -> Iterable[T]:
        return list(self._items.values())
