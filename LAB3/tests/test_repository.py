"""Extended tests for BookingRepository and InMemoryRepository."""
import pytest

from airport_system.repositories.base import InMemoryRepository
from airport_system.repositories.booking_repository import BookingRepository
from airport_system.domain.booking import Booking
from airport_system.exceptions import BookingNotFoundError


class TestInMemoryRepository:
    """Tests for InMemoryRepository base class."""

    def test_add_and_get(self):
        """Test adding and retrieving item."""
        repo = InMemoryRepository[str]()
        repo.add("key1", "value1")
        assert repo.get("key1") == "value1"

    def test_get_nonexistent(self):
        """Test getting non-existent key returns None."""
        repo = InMemoryRepository[str]()
        assert repo.get("nonexistent") is None

    def test_remove(self):
        """Test removing item."""
        repo = InMemoryRepository[str]()
        repo.add("key1", "value1")
        assert repo.get("key1") is not None
        repo.remove("key1")
        assert repo.get("key1") is None

    def test_remove_nonexistent(self):
        """Test removing non-existent key (should not raise)."""
        repo = InMemoryRepository[str]()
        repo.remove("nonexistent")  # Should not raise

    def test_all(self):
        """Test getting all items."""
        repo = InMemoryRepository[str]()
        repo.add("key1", "value1")
        repo.add("key2", "value2")
        repo.add("key3", "value3")
        all_items = repo.all()
        assert len(all_items) == 3
        assert "value1" in all_items
        assert "value2" in all_items
        assert "value3" in all_items


class TestBookingRepository:
    """Tests for BookingRepository."""

    def test_find_by_passenger(self):
        """Test finding bookings by passenger ID."""
        repo = BookingRepository()
        b1 = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        b2 = Booking(booking_id="B2", passenger_id="P1", flight_id="F2")
        b3 = Booking(booking_id="B3", passenger_id="P2", flight_id="F3")
        repo.add("B1", b1)
        repo.add("B2", b2)
        repo.add("B3", b3)
        
        bookings = repo.find_by_passenger("P1")
        assert len(bookings) == 2
        assert all(b.passenger_id == "P1" for b in bookings)

    def test_find_by_passenger_none_found(self):
        """Test finding bookings by passenger ID when none exist."""
        repo = BookingRepository()
        b1 = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        repo.add("B1", b1)
        
        bookings = repo.find_by_passenger("P999")
        assert bookings == []

    def test_get_required_success(self):
        """Test get_required returns booking when exists."""
        repo = BookingRepository()
        b1 = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        repo.add("B1", b1)
        
        booking = repo.get_required("B1")
        assert booking.booking_id == "B1"

    def test_get_required_not_found(self):
        """Test get_required raises error when not found."""
        repo = BookingRepository()
        
        with pytest.raises(BookingNotFoundError):
            repo.get_required("NONEXISTENT")
