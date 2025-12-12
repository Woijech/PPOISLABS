"""Tests for AirportStatistics domain model."""
from airport_system.domain.statistics import AirportStatistics


def test_airport_statistics_basic():
    """Test basic AirportStatistics creation."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=1000000,
        total_flights=10000,
        total_cargo_tons=50000.0,
        avg_delay_minutes=15.5,
        cancelled_flights=200,
        diverted_flights=50,
        on_time_flights=8000,
        international_flights=3000,
        domestic_flights=7000,
        security_incidents=5,
        lost_baggage_items=100,
        handled_baggage_items=500000,
        vip_passengers=5000,
        loyalty_gold=20000,
        loyalty_platinum=5000,
        checkin_counters=100,
        security_checkpoints=20,
        terminals=4,
        gates=80,
        runways=3,
        max_daily_flights=300,
        max_daily_passengers=35000,
        avg_load_factor=85.5,
        fuel_consumption_tons=10000.0
    )
    assert stats.year == 2024
    assert stats.total_passengers == 1000000
    assert stats.total_flights == 10000


def test_on_time_percents():
    """Test on-time percentage calculation."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=10000,
        total_flights=100,
        total_cargo_tons=100.0,
        avg_delay_minutes=10.0,
        cancelled_flights=5,
        diverted_flights=2,
        on_time_flights=80,
        international_flights=30,
        domestic_flights=70,
        security_incidents=0,
        lost_baggage_items=10,
        handled_baggage_items=1000,
        vip_passengers=100,
        loyalty_gold=500,
        loyalty_platinum=100,
        checkin_counters=20,
        security_checkpoints=5,
        terminals=2,
        gates=20,
        runways=1,
        max_daily_flights=50,
        max_daily_passengers=5000,
        avg_load_factor=75.0,
        fuel_consumption_tons=500.0
    )
    assert stats.on_time_percents() == 80.0


def test_on_time_percents_zero_flights():
    """Test on-time percentage with zero flights."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=0,
        total_flights=0,
        total_cargo_tons=0.0,
        avg_delay_minutes=0.0,
        cancelled_flights=0,
        diverted_flights=0,
        on_time_flights=0,
        international_flights=0,
        domestic_flights=0,
        security_incidents=0,
        lost_baggage_items=0,
        handled_baggage_items=0,
        vip_passengers=0,
        loyalty_gold=0,
        loyalty_platinum=0,
        checkin_counters=0,
        security_checkpoints=0,
        terminals=0,
        gates=0,
        runways=0,
        max_daily_flights=0,
        max_daily_passengers=0,
        avg_load_factor=0.0,
        fuel_consumption_tons=0.0
    )
    assert stats.on_time_percents() == 0.0


def test_baggage_loss_rate():
    """Test baggage loss rate calculation."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=10000,
        total_flights=100,
        total_cargo_tons=100.0,
        avg_delay_minutes=10.0,
        cancelled_flights=5,
        diverted_flights=2,
        on_time_flights=80,
        international_flights=30,
        domestic_flights=70,
        security_incidents=0,
        lost_baggage_items=10,
        handled_baggage_items=1000,
        vip_passengers=100,
        loyalty_gold=500,
        loyalty_platinum=100,
        checkin_counters=20,
        security_checkpoints=5,
        terminals=2,
        gates=20,
        runways=1,
        max_daily_flights=50,
        max_daily_passengers=5000,
        avg_load_factor=75.0,
        fuel_consumption_tons=500.0
    )
    assert stats.baggage_loss_rate() == 1.0


def test_baggage_loss_rate_zero_handled():
    """Test baggage loss rate with zero handled items."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=0,
        total_flights=0,
        total_cargo_tons=0.0,
        avg_delay_minutes=0.0,
        cancelled_flights=0,
        diverted_flights=0,
        on_time_flights=0,
        international_flights=0,
        domestic_flights=0,
        security_incidents=0,
        lost_baggage_items=0,
        handled_baggage_items=0,
        vip_passengers=0,
        loyalty_gold=0,
        loyalty_platinum=0,
        checkin_counters=0,
        security_checkpoints=0,
        terminals=0,
        gates=0,
        runways=0,
        max_daily_flights=0,
        max_daily_passengers=0,
        avg_load_factor=0.0,
        fuel_consumption_tons=0.0
    )
    assert stats.baggage_loss_rate() == 0.0


def test_average_passengers_per_flight():
    """Test average passengers per flight calculation."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=10000,
        total_flights=100,
        total_cargo_tons=100.0,
        avg_delay_minutes=10.0,
        cancelled_flights=5,
        diverted_flights=2,
        on_time_flights=80,
        international_flights=30,
        domestic_flights=70,
        security_incidents=0,
        lost_baggage_items=10,
        handled_baggage_items=1000,
        vip_passengers=100,
        loyalty_gold=500,
        loyalty_platinum=100,
        checkin_counters=20,
        security_checkpoints=5,
        terminals=2,
        gates=20,
        runways=1,
        max_daily_flights=50,
        max_daily_passengers=5000,
        avg_load_factor=75.0,
        fuel_consumption_tons=500.0
    )
    assert stats.average_passengers_per_flight() == 100.0


def test_average_passengers_per_flight_zero_flights():
    """Test average passengers per flight with zero flights."""
    stats = AirportStatistics(
        year=2024,
        total_passengers=0,
        total_flights=0,
        total_cargo_tons=0.0,
        avg_delay_minutes=0.0,
        cancelled_flights=0,
        diverted_flights=0,
        on_time_flights=0,
        international_flights=0,
        domestic_flights=0,
        security_incidents=0,
        lost_baggage_items=0,
        handled_baggage_items=0,
        vip_passengers=0,
        loyalty_gold=0,
        loyalty_platinum=0,
        checkin_counters=0,
        security_checkpoints=0,
        terminals=0,
        gates=0,
        runways=0,
        max_daily_flights=0,
        max_daily_passengers=0,
        avg_load_factor=0.0,
        fuel_consumption_tons=0.0
    )
    assert stats.average_passengers_per_flight() == 0.0
