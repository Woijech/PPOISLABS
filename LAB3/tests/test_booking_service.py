from airport_system.domain.enums import BookingStatus
from airport_system.repositories.booking_repository import BookingRepository
from airport_system.services.booking_service import BookingService
from airport_system.exceptions import BookingAlreadyPaidError, BookingNotFoundError


def test_create_confirm_and_cancel_booking():
    repo = BookingRepository()
    service = BookingService(bookings=repo)

    booking = service.create_booking("P1", "F1")
    assert booking.status == BookingStatus.CREATED

    confirmed = service.confirm_booking(booking.booking_id)
    assert confirmed.status == BookingStatus.CONFIRMED

    cancelled = service.cancel_booking(booking.booking_id)
    assert cancelled.status == BookingStatus.CANCELLED

def test_mark_paid_and_not_found():
    repo = BookingRepository()
    service = BookingService(bookings=repo)

    booking = service.create_booking("P1", "F1")
    service.confirm_booking(booking.booking_id)
    paid = service.mark_paid(booking.booking_id, "PAY1")
    assert paid.status == BookingStatus.COMPLETED
    assert "PAY1" in paid.payment_ids

    try:
        service.mark_paid("UNKNOWN", "PAY2")
    except BookingNotFoundError:
        pass
    else:
        assert False

def test_mark_paid_for_finalised_booking_raises():
    repo = BookingRepository()
    service = BookingService(bookings=repo)

    booking = service.create_booking("P1", "F1")
    service.confirm_booking(booking.booking_id)
    service.mark_paid(booking.booking_id, "PAY1")

    try:
        service.mark_paid(booking.booking_id, "PAY2")
    except BookingAlreadyPaidError:
        pass
    else:
        assert False

def test_get_bookings_for_passenger():
    repo = BookingRepository()
    service = BookingService(bookings=repo)
    b1 = service.create_booking("P1", "F1")
    b2 = service.create_booking("P1", "F2")
    service.create_booking("P2", "F3")
    bookings = service.get_bookings_for_passenger("P1")
    ids = {b.booking_id for b in bookings}
    assert b1.booking_id in ids and b2.booking_id in ids
