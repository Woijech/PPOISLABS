from datetime import datetime, timedelta, date

from airport_system.domain.aircraft import Aircraft, Seat
from airport_system.domain.baggage import BaggageItem, BaggageTag
from airport_system.domain.booking import Booking
from airport_system.domain.enums import (
    BaggageStatus,
    BookingStatus,
    FlightStatus,
    SeatClass,
    SecurityLevel,
)
from airport_system.domain.flight import Flight
from airport_system.domain.passenger import ContactInfo, LoyaltyAccount, Passenger
from airport_system.domain.payment import Money
from airport_system.domain.terminal import BoardingPass, Gate, Terminal
from airport_system.domain.security import AccessBadge, SecurityCheckpoint
from airport_system.domain.schedule import AirportSchedule


def test_passenger_and_loyalty_and_password():
    contact = ContactInfo(email="user@example.com", phone="+123", address="Main st")
    passenger = Passenger(passenger_id="P1", name="Test Passenger", contact=contact, nationality="US")
    passenger.set_password("secret")
    assert passenger.verify_password("secret")
    passenger.date_of_birth = date(2000, 1, 1)
    assert passenger.age() is not None
    account = LoyaltyAccount(number="L1")
    passenger.link_loyalty(account)
    passenger.loyalty.add_points(10000)
    assert passenger.loyalty.points == 10000
    assert passenger.loyalty.tier in {"BRONZE", "SILVER", "GOLD", "PLATINUM"}

def test_aircraft_and_seats():
    aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6100)
    seat = Seat(seat_number="1A", seat_class=SeatClass.FIRST, is_exit_row=True)
    aircraft.add_seat(seat)
    assert len(aircraft.available_seats()) == 1
    seat.reserve()
    assert len(aircraft.available_seats()) == 0
    seat.release()
    assert len(aircraft.available_seats()) == 1
    assert seat.is_premium()
    assert aircraft.is_long_haul()

def test_booking_and_boarding_pass():
    booking = Booking(booking_id="B1", passenger_id="P1", flight_id="F1", refundable=True)
    booking.confirm()
    booking.add_ticket("T1")
    money = Money(amount=100.0)
    assert booking.status == BookingStatus.CONFIRMED
    assert "T1" in booking.ticket_ids
    assert booking.is_refundable()
    gate = Gate(gate_id="G1", terminal_code="T1")
    terminal = Terminal(code="T1", gates=[gate])
    bp = BoardingPass(
        boarding_pass_id="BP1",
        booking_id=booking.booking_id,
        passenger_name="Name",
        gate_id=gate.gate_id,
        seat_number="1A",
    )
    bp.change_gate("G2")
    assert bp.gate_id == "G2"
    assert terminal.available_gates_count() == 1

def test_baggage_states_and_volume():
    tag = BaggageTag(tag_id="TAG1", booking_id="B1")
    item = BaggageItem(tag=tag, weight_kg=20.0, length_cm=50, width_cm=40, height_cm=20)
    item.check_in("SFO")
    assert item.status == BaggageStatus.CHECKED_IN
    item.mark_loaded("BELT")
    assert item.status == BaggageStatus.LOADED
    item.mark_lost()
    assert item.status == BaggageStatus.LOST
    assert item.volume_liters() > 0
    assert item.is_oversized(100) is True

def test_flight_lifecycle_and_gate_and_schedule():
    aircraft = Aircraft(registration="R1", model="A320", manufacturer="Airbus", range_km=6100)
    seat = Seat(seat_number="1A", seat_class=SeatClass.ECONOMY)
    aircraft.add_seat(seat)
    now = datetime.now()
    flight = Flight(
        flight_id="FL1",
        origin="SFO",
        destination="LAX",
        departure_time=now,
        arrival_time=now + timedelta(hours=2),
        aircraft=aircraft,
        distance_km=550,
    )
    flight.assign_gate("G1", "T1")
    assert flight.gate_id == "G1"
    flight.delay(10)
    assert flight.status == FlightStatus.DELAYED
    duration = flight.flight_duration_hours()
    assert duration > 0
    flight.depart()
    assert flight.status == FlightStatus.DEPARTED
    flight.arrive()
    assert flight.status == FlightStatus.ARRIVED

    schedule = AirportSchedule()
    schedule.add_flight(flight)
    assert schedule.total_flights() == 1

def test_security_and_checkpoint_basic():
    badge = AccessBadge(badge_id="B1", owner_id="E1", level=SecurityLevel.STAFF)
    checkpoint = SecurityCheckpoint(checkpoint_id="C1", required_level=SecurityLevel.PUBLIC, name="Main")
    assert checkpoint.can_pass(badge)
    badge.revoke()
    assert not checkpoint.can_pass(badge)
