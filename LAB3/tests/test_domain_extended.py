"""Extended tests for Aircraft, Seat, Flight, Booking models."""
import pytest
from datetime import datetime, timedelta

from airport_system.domain.aircraft import Aircraft, Seat
from airport_system.domain.flight import Flight
from airport_system.domain.booking import Booking
from airport_system.domain.enums import SeatClass, FlightStatus, BookingStatus


class TestSeatExtended:
    """Extended tests for Seat class."""

    def test_seat_reserve_already_reserved(self):
        """Test reserving already reserved seat raises error."""
        seat = Seat(seat_number="1A", seat_class=SeatClass.FIRST)
        seat.reserve()
        with pytest.raises(ValueError, match="Seat already reserved"):
            seat.reserve()

    def test_seat_is_premium_economy(self):
        """Test economy seat is not premium."""
        seat = Seat(seat_number="10A", seat_class=SeatClass.ECONOMY)
        assert seat.is_premium() is False

    def test_seat_is_premium_premium_economy(self):
        """Test premium economy seat is not premium."""
        seat = Seat(seat_number="5A", seat_class=SeatClass.PREMIUM_ECONOMY)
        assert seat.is_premium() is False

    def test_seat_is_premium_business(self):
        """Test business seat is premium."""
        seat = Seat(seat_number="2A", seat_class=SeatClass.BUSINESS)
        assert seat.is_premium() is True


class TestAircraftExtended:
    """Extended tests for Aircraft class."""

    def test_aircraft_add_flight_hours_invalid(self):
        """Test adding zero or negative hours raises error."""
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
        with pytest.raises(ValueError, match="Hours must be positive"):
            aircraft.add_flight_hours(0)
        with pytest.raises(ValueError, match="Hours must be positive"):
            aircraft.add_flight_hours(-10)

    def test_aircraft_add_flight_hours_valid(self):
        """Test adding valid flight hours."""
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
        aircraft.add_flight_hours(100)
        assert aircraft.flight_hours == 100
        aircraft.add_flight_hours(50)
        assert aircraft.flight_hours == 150

    def test_aircraft_retire(self):
        """Test retiring aircraft."""
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
        assert aircraft.in_service is True
        aircraft.retire()
        assert aircraft.in_service is False

    def test_aircraft_is_long_haul_false(self):
        """Test short-haul aircraft."""
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=3000)
        assert aircraft.is_long_haul() is False


class TestFlightExtended:
    """Extended tests for Flight class."""

    def test_flight_delay_invalid(self):
        """Test delaying with zero or negative minutes raises error."""
        aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6000)
        now = datetime.now()
        flight = Flight(
            flight_id="FL1",
            origin="SFO",
            destination="LAX",
            departure_time=now,
            arrival_time=now + timedelta(hours=2),
            aircraft=aircraft,
            distance_km=500
        )
        with pytest.raises(ValueError, match="Delay minutes must be positive"):
            flight.delay(0)
        with pytest.raises(ValueError, match="Delay minutes must be positive"):
            flight.delay(-10)


class TestBookingExtended:
    """Extended tests for Booking class."""

    def test_booking_confirm_already_confirmed(self):
        """Test confirming already confirmed booking raises error."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.confirm()
        with pytest.raises(ValueError, match="Only newly created bookings can be confirmed"):
            booking.confirm()

    def test_booking_cancel_already_cancelled(self):
        """Test canceling already cancelled booking raises error."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.cancel()
        with pytest.raises(ValueError, match="Booking already finalized"):
            booking.cancel()

    def test_booking_cancel_completed(self):
        """Test canceling completed booking raises error."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.status = BookingStatus.COMPLETED
        with pytest.raises(ValueError, match="Booking already finalized"):
            booking.cancel()

    def test_booking_add_payment(self):
        """Test adding payment to booking."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.add_payment("PAY1")
        assert "PAY1" in booking.payment_ids
        # Adding same payment again should not duplicate
        booking.add_payment("PAY1")
        assert booking.payment_ids.count("PAY1") == 1

    def test_booking_add_ticket_no_duplicate(self):
        """Test adding same ticket twice doesn't duplicate."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.add_ticket("T1")
        booking.add_ticket("T1")
        assert booking.ticket_ids.count("T1") == 1

    def test_booking_mark_checked_in(self):
        """Test marking booking as checked in."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        booking.mark_checked_in()
        assert booking.status == BookingStatus.CHECKED_IN

    def test_booking_is_refundable_false_not_refundable(self):
        """Test is_refundable when refundable=False."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1", refundable=False)
        booking.confirm()
        assert booking.is_refundable() is False

    def test_booking_is_refundable_false_cancelled(self):
        """Test is_refundable for cancelled booking."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1", refundable=True)
        booking.cancel()
        assert booking.is_refundable() is False

    def test_booking_has_payments(self):
        """Test has_payments method."""
        booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1")
        assert booking.has_payments() is False
        booking.add_payment("PAY1")
        assert booking.has_payments() is True
