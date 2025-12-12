"""Tests for AppConfig."""
from airport_system.config import AppConfig


def test_app_config_default():
    """Test default AppConfig creation."""
    config = AppConfig.default()
    assert config.airport_name == "Demo Airport"
    assert config.timezone == "UTC"
    assert config.default_currency == "USD"
    assert config.support_email == "support@example.com"
    assert config.max_baggage_weight == 32.0


def test_app_config_baggage_limit():
    """Test baggage limit method."""
    config = AppConfig(
        airport_name="Test Airport",
        timezone="UTC",
        max_baggage_weight=25.0
    )
    assert config.baggage_limit_kg() == 25.0


def test_app_config_custom():
    """Test custom AppConfig creation."""
    config = AppConfig(
        airport_name="Custom Airport",
        timezone="Europe/Moscow",
        default_currency="EUR",
        support_email="help@airport.com",
        max_baggage_weight=30.0
    )
    assert config.airport_name == "Custom Airport"
    assert config.timezone == "Europe/Moscow"
    assert config.default_currency == "EUR"
    assert config.support_email == "help@airport.com"
    assert config.max_baggage_weight == 30.0
