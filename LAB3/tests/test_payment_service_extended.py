"""Extended tests for PaymentService."""
import pytest

from airport_system.domain.payment import CardPayment, Money, Payment
from airport_system.domain.enums import PaymentStatus
from airport_system.services.payment_service import PaymentService
from airport_system.exceptions import CurrencyMismatchError, InsufficientFundsError, PaymentDeclinedError


class TestPaymentServiceChargeCard:
    """Tests for PaymentService.charge_card method."""

    def test_charge_card_success(self):
        """Test successful card charge."""
        service = PaymentService(currency="USD")
        amount = Money(amount=100.0, currency="USD")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        payment = service.charge_card("BKG1", amount, card)
        assert payment.status == PaymentStatus.COMPLETED
        assert payment.booking_id == "BKG1"
        assert payment.amount.amount == 100.0

    def test_charge_card_currency_mismatch(self):
        """Test charge with mismatched currency."""
        service = PaymentService(currency="USD")
        amount = Money(amount=100.0, currency="EUR")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        with pytest.raises(CurrencyMismatchError):
            service.charge_card("BKG1", amount, card)

    def test_charge_card_zero_amount(self):
        """Test charge with zero amount."""
        service = PaymentService(currency="USD")
        amount = Money(amount=0.0, currency="USD")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        with pytest.raises(InsufficientFundsError):
            service.charge_card("BKG1", amount, card)

    def test_charge_card_negative_amount(self):
        """Test charge with negative amount."""
        service = PaymentService(currency="USD")
        amount = Money(amount=-50.0, currency="USD")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        with pytest.raises(InsufficientFundsError):
            service.charge_card("BKG1", amount, card)

    def test_charge_card_declined(self):
        """Test charge when card authorization fails."""
        service = PaymentService(currency="USD")
        amount = Money(amount=15000.0, currency="USD")  # Exceeds card limit
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        with pytest.raises(PaymentDeclinedError):
            service.charge_card("BKG1", amount, card)


class TestPaymentServiceRefund:
    """Tests for PaymentService.refund_payment method."""

    def test_refund_payment_success(self):
        """Test successful payment refund."""
        service = PaymentService(currency="USD")
        amount = Money(amount=100.0, currency="USD")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        payment = service.charge_card("BKG1", amount, card)
        refunded = service.refund_payment(payment)
        assert refunded.status == PaymentStatus.REFUNDED

    def test_refund_pending_payment_raises(self):
        """Test refund of pending payment raises error."""
        service = PaymentService(currency="USD")
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount,
            status=PaymentStatus.PENDING
        )
        with pytest.raises(PaymentDeclinedError):
            service.refund_payment(payment)


class TestPaymentServiceSplitPayment:
    """Tests for PaymentService.split_payment method."""

    def test_split_payment_success(self):
        """Test successful split payment."""
        service = PaymentService(currency="USD")
        total = Money(amount=300.0, currency="USD")
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        payments = service.split_payment("BKG1", total, 3, card)
        assert len(payments) == 3
        assert all(p.status == PaymentStatus.COMPLETED for p in payments)
        assert all(p.amount.amount == 100.0 for p in payments)


class TestPaymentServiceTransfer:
    """Tests for PaymentService.transfer_between_cards method."""

    def test_transfer_success(self):
        """Test successful transfer between cards."""
        service = PaymentService(currency="USD")
        from_card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        to_card = CardPayment(
            card_number="6543210987654321",
            holder_name="Jane Doe",
            expiration="12/26"
        )
        amount = Money(amount=500.0, currency="USD")
        result = service.transfer_between_cards(from_card, to_card, amount)
        assert result is True

    def test_transfer_currency_mismatch(self):
        """Test transfer with mismatched currency."""
        service = PaymentService(currency="USD")
        from_card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        to_card = CardPayment(
            card_number="6543210987654321",
            holder_name="Jane Doe",
            expiration="12/26"
        )
        amount = Money(amount=500.0, currency="EUR")
        with pytest.raises(CurrencyMismatchError):
            service.transfer_between_cards(from_card, to_card, amount)

    def test_transfer_source_declined(self):
        """Test transfer when source card authorization fails."""
        service = PaymentService(currency="USD")
        from_card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        to_card = CardPayment(
            card_number="6543210987654321",
            holder_name="Jane Doe",
            expiration="12/26"
        )
        amount = Money(amount=15000.0, currency="USD")  # Exceeds limit
        with pytest.raises(PaymentDeclinedError):
            service.transfer_between_cards(from_card, to_card, amount)
