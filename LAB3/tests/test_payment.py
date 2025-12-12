"""Extended tests for Money, CardPayment, and Payment models."""
import pytest

from airport_system.domain.payment import Money, CardPayment, Payment
from airport_system.domain.enums import PaymentStatus


class TestMoney:
    """Tests for Money class."""

    def test_money_basic(self):
        """Test basic Money creation."""
        money = Money(amount=100.0, currency="USD")
        assert money.amount == 100.0
        assert money.currency == "USD"
        assert money.precision == 2

    def test_money_allocate(self):
        """Test allocating money into parts."""
        money = Money(amount=100.0, currency="USD")
        share = money.allocate(4)
        assert share == 25.0

    def test_money_allocate_zero_parts_raises(self):
        """Test allocating with zero parts raises error."""
        money = Money(amount=100.0, currency="USD")
        with pytest.raises(ValueError, match="Parts must be positive"):
            money.allocate(0)

    def test_money_allocate_negative_parts_raises(self):
        """Test allocating with negative parts raises error."""
        money = Money(amount=100.0, currency="USD")
        with pytest.raises(ValueError, match="Parts must be positive"):
            money.allocate(-5)

    def test_money_add(self):
        """Test adding two Money objects."""
        m1 = Money(amount=100.0, currency="USD")
        m2 = Money(amount=50.0, currency="USD")
        result = m1.add(m2)
        assert result.amount == 150.0
        assert result.currency == "USD"

    def test_money_add_currency_mismatch(self):
        """Test adding with different currencies raises error."""
        m1 = Money(amount=100.0, currency="USD")
        m2 = Money(amount=50.0, currency="EUR")
        with pytest.raises(ValueError, match="Currency mismatch"):
            m1.add(m2)

    def test_money_subtract(self):
        """Test subtracting two Money objects."""
        m1 = Money(amount=100.0, currency="USD")
        m2 = Money(amount=30.0, currency="USD")
        result = m1.subtract(m2)
        assert result.amount == 70.0
        assert result.currency == "USD"

    def test_money_subtract_currency_mismatch(self):
        """Test subtracting with different currencies raises error."""
        m1 = Money(amount=100.0, currency="USD")
        m2 = Money(amount=30.0, currency="EUR")
        with pytest.raises(ValueError, match="Currency mismatch"):
            m1.subtract(m2)

    def test_money_percentage(self):
        """Test percentage calculation."""
        money = Money(amount=200.0, currency="USD")
        result = money.percentage(10.0)
        assert result.amount == 20.0
        assert result.currency == "USD"


class TestCardPayment:
    """Tests for CardPayment class."""

    def test_card_payment_basic(self):
        """Test basic CardPayment creation."""
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        assert card.card_number == "1234567890123456"
        assert card.holder_name == "John Doe"
        assert card.expiration == "12/25"

    def test_card_authorize_valid(self):
        """Test authorizing valid amount with valid card."""
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        amount = Money(amount=500.0, currency="USD")
        assert card.authorize(amount) is True

    def test_card_authorize_amount_too_high(self):
        """Test authorizing with amount exceeding limit."""
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        amount = Money(amount=15000.0, currency="USD")
        assert card.authorize(amount) is False

    def test_card_authorize_invalid_card_length(self):
        """Test authorizing with invalid card number length."""
        card = CardPayment(
            card_number="1234",
            holder_name="John Doe",
            expiration="12/25"
        )
        amount = Money(amount=100.0, currency="USD")
        assert card.authorize(amount) is False

    def test_card_authorize_valid_amex_15_digits(self):
        """Test authorizing with 15-digit AMEX card."""
        card = CardPayment(
            card_number="123456789012345",
            holder_name="John Doe",
            expiration="12/25"
        )
        amount = Money(amount=100.0, currency="USD")
        assert card.authorize(amount) is True

    def test_masked_number_normal(self):
        """Test masking normal card number."""
        card = CardPayment(
            card_number="1234567890123456",
            holder_name="John Doe",
            expiration="12/25"
        )
        masked = card.masked_number()
        assert masked == "************3456"
        assert len(masked) == 16

    def test_masked_number_short(self):
        """Test masking short card number."""
        card = CardPayment(
            card_number="123",
            holder_name="John Doe",
            expiration="12/25"
        )
        masked = card.masked_number()
        assert masked == "***"


class TestPayment:
    """Tests for Payment class."""

    def test_payment_basic(self):
        """Test basic Payment creation."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        assert payment.payment_id == "PAY1"
        assert payment.booking_id == "BKG1"
        assert payment.status == PaymentStatus.PENDING
        assert payment.provider == "CARD"

    def test_payment_mark_completed(self):
        """Test marking payment as completed."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        payment.mark_completed()
        assert payment.status == PaymentStatus.COMPLETED

    def test_payment_mark_declined(self):
        """Test marking payment as declined."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        payment.mark_declined()
        assert payment.status == PaymentStatus.DECLINED

    def test_payment_mark_refunded(self):
        """Test marking payment as refunded."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        payment.mark_completed()
        payment.mark_refunded()
        assert payment.status == PaymentStatus.REFUNDED

    def test_payment_is_successful_true(self):
        """Test is_successful returns true for completed payment."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        payment.mark_completed()
        assert payment.is_successful() is True

    def test_payment_is_successful_false(self):
        """Test is_successful returns false for pending payment."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        assert payment.is_successful() is False

    def test_payment_add_metadata(self):
        """Test adding metadata to payment."""
        amount = Money(amount=100.0, currency="USD")
        payment = Payment(
            payment_id="PAY1",
            booking_id="BKG1",
            amount=amount
        )
        payment.add_metadata("transaction_id", "TXN123")
        payment.add_metadata("gateway", "stripe")
        assert payment.metadata["transaction_id"] == "TXN123"
        assert payment.metadata["gateway"] == "stripe"
