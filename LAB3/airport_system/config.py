from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AppConfig:
    airport_name: str
    timezone: str
    default_currency: str = "USD"
    support_email: str = "support@example.com"
    max_baggage_weight: float = 32.0

    @classmethod
    def default(cls) -> "AppConfig":
        return cls(airport_name="Demo Airport", timezone="UTC")

    def baggage_limit_kg(self) -> float:
        return self.max_baggage_weight
