"""Tests for Ticket domain model."""
import pytest

from airport_system.domain.ticket import Ticket
from airport_system.domain.enums import SeatClass


def test_ticket_basic():
    """Test basic Ticket creation."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.BUSINESS,
        base_price=500.0,
        fare_basis="YBUSINESS",
        booking_class="Y"
    )
    assert ticket.ticket_id == "T1"
    assert ticket.passenger_id == "P1"
    assert ticket.flight_id == "F1"
    assert ticket.seat_number == "1A"
    assert ticket.base_price == 500.0
    assert ticket.checked_in is False


def test_ticket_mark_checked_in():
    """Test checking in a ticket."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0
    )
    assert ticket.checked_in is False
    ticket.mark_checked_in()
    assert ticket.checked_in is True


def test_ticket_calculate_price_with_tax():
    """Test price calculation with tax."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0
    )
    price_with_tax = ticket.calculate_price_with_tax(0.1)
    assert abs(price_with_tax - 110.0) < 0.001


def test_ticket_calculate_price_with_zero_tax():
    """Test price calculation with zero tax."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0
    )
    price_with_tax = ticket.calculate_price_with_tax(0.0)
    assert price_with_tax == 100.0


def test_ticket_calculate_price_negative_tax_raises():
    """Test that negative tax rate raises ValueError."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0
    )
    with pytest.raises(ValueError, match="Tax rate must be non-negative"):
        ticket.calculate_price_with_tax(-0.1)


def test_ticket_is_upgradeable_economy():
    """Test that economy class ticket is upgradeable."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0
    )
    assert ticket.is_upgradeable() is True


def test_ticket_is_upgradeable_premium_economy():
    """Test that premium economy class ticket is upgradeable."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.PREMIUM_ECONOMY,
        base_price=200.0
    )
    assert ticket.is_upgradeable() is True


def test_ticket_is_upgradeable_business():
    """Test that business class ticket is not upgradeable."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.BUSINESS,
        base_price=500.0
    )
    assert ticket.is_upgradeable() is False


def test_ticket_is_upgradeable_first():
    """Test that first class ticket is not upgradeable."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.FIRST,
        base_price=1000.0
    )
    assert ticket.is_upgradeable() is False


def test_ticket_can_refund_refundable_not_checked_in():
    """Test refund for refundable ticket not checked in."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0,
        refundable=True
    )
    assert ticket.can_refund() is True


def test_ticket_can_refund_refundable_checked_in():
    """Test refund for refundable ticket that is checked in."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0,
        refundable=True
    )
    ticket.mark_checked_in()
    assert ticket.can_refund() is False


def test_ticket_can_refund_non_refundable():
    """Test refund for non-refundable ticket."""
    ticket = Ticket(
        ticket_id="T1",
        passenger_id="P1",
        flight_id="F1",
        seat_number="1A",
        seat_class=SeatClass.ECONOMY,
        base_price=100.0,
        refundable=False
    )
    assert ticket.can_refund() is False
