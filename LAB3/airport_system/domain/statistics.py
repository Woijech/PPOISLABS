from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AirportStatistics:
    year: int
    total_passengers: int
    total_flights: int
    total_cargo_tons: float
    avg_delay_minutes: float
    cancelled_flights: int
    diverted_flights: int
    on_time_flights: int
    international_flights: int
    domestic_flights: int
    security_incidents: int
    lost_baggage_items: int
    handled_baggage_items: int
    vip_passengers: int
    loyalty_gold: int
    loyalty_platinum: int
    checkin_counters: int
    security_checkpoints: int
    terminals: int
    gates: int
    runways: int
    max_daily_flights: int
    max_daily_passengers: int
    avg_load_factor: float
    fuel_consumption_tons: float

    def on_time_percents(self) -> float:
        if self.total_flights == 0:
            return 0.0
        return round(self.on_time_flights / self.total_flights * 100.0, 2)

    def baggage_loss_rate(self) -> float:
        if self.handled_baggage_items == 0:
            return 0.0
        return round(self.lost_baggage_items / self.handled_baggage_items * 100.0, 3)

    def average_passengers_per_flight(self) -> float:
        if self.total_flights == 0:
            return 0.0
        return round(self.total_passengers / self.total_flights, 2)
