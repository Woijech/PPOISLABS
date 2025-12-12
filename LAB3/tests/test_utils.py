"""Tests for utility modules: time_utils, validation, id_generator."""
from datetime import datetime, timezone

import pytest

from airport_system.utils.time_utils import now_utc, to_iso
from airport_system.utils.validation import ensure_not_empty, ensure_positive


def test_now_utc():
    """Test now_utc returns UTC datetime."""
    dt = now_utc()
    assert isinstance(dt, datetime)
    assert dt.tzinfo == timezone.utc


def test_to_iso():
    """Test to_iso converts datetime to ISO string."""
    dt = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
    iso_str = to_iso(dt)
    assert "2024-01-15" in iso_str
    assert "10:30:00" in iso_str


def test_to_iso_naive_datetime():
    """Test to_iso with naive datetime."""
    dt = datetime(2024, 1, 15, 10, 30, 0)
    # Will assume local timezone and convert to UTC
    iso_str = to_iso(dt)
    assert "2024-01-15" in iso_str or "2024-01-14" in iso_str  # Depends on timezone


def test_ensure_not_empty_valid():
    """Test ensure_not_empty with valid string."""
    # Should not raise
    ensure_not_empty("hello", "test_field")


def test_ensure_not_empty_empty_string():
    """Test ensure_not_empty with empty string raises ValueError."""
    with pytest.raises(ValueError, match="test_field must not be empty"):
        ensure_not_empty("", "test_field")


def test_ensure_not_empty_with_different_field_name():
    """Test ensure_not_empty shows correct field name in error message."""
    with pytest.raises(ValueError, match="field_name must not be empty"):
        ensure_not_empty("", "field_name")


def test_ensure_positive_valid():
    """Test ensure_positive with positive number."""
    # Should not raise
    ensure_positive(5.0, "test_field")
    ensure_positive(0.001, "test_field")


def test_ensure_positive_zero():
    """Test ensure_positive with zero raises ValueError."""
    with pytest.raises(ValueError, match="test_field must be positive"):
        ensure_positive(0, "test_field")


def test_ensure_positive_negative():
    """Test ensure_positive with negative number raises ValueError."""
    with pytest.raises(ValueError, match="test_field must be positive"):
        ensure_positive(-5.0, "test_field")
