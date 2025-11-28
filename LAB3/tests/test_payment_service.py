from airport_system.domain.payment import CardPayment, Money, Payment
from airport_system.domain.enums import PaymentStatus
from airport_system.exceptions import CurrencyMismatchError, InsufficientFundsError, PaymentDeclinedError
from airport_system.services.payment_service import PaymentService


def test_successful_card_payment_and_refund():
    service = PaymentService(currency="USD")
    card = CardPayment(card_number="4111111111111111", holder_name="Test User", expiration="12/30")
    amount = Money(amount=100.0, currency="USD")
    payment = service.charge_card("BKG1", amount, card)
    assert payment.is_successful()

    refunded = service.refund_payment(payment)
    assert refunded.status == PaymentStatus.REFUNDED

def test_currency_mismatch_raises():
    service = PaymentService(currency="USD")
    card = CardPayment(card_number="4111111111111111", holder_name="Test User", expiration="12/30")
    amount = Money(amount=100.0, currency="EUR")
    try:
        service.charge_card("BKG1", amount, card)
    except CurrencyMismatchError:
        pass
    else:
        assert False

def test_declined_card_raises():
    service = PaymentService(currency="USD")
    card = CardPayment(card_number="123", holder_name="Test User", expiration="12/30")
    amount = Money(amount=100.0, currency="USD")
    try:
        service.charge_card("BKG1", amount, card)
    except PaymentDeclinedError:
        pass
    else:
        assert False

def test_negative_amount_raises():
    service = PaymentService(currency="USD")
    card = CardPayment(card_number="4111111111111111", holder_name="Test User", expiration="12/30")
    amount = Money(amount=-1.0, currency="USD")
    try:
        service.charge_card("BKG1", amount, card)
    except InsufficientFundsError:
        pass
    else:
        assert False

def test_transfer_between_cards():
    service = PaymentService(currency="USD")
    from_card = CardPayment(card_number="4111111111111111", holder_name="From", expiration="11/30")
    to_card = CardPayment(card_number="5500000000000004", holder_name="To", expiration="10/30")
    amount = Money(amount=50.0, currency="USD")
    assert service.transfer_between_cards(from_card, to_card, amount) is True
