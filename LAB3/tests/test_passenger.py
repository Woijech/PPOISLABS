"""Extended tests for Passenger, ContactInfo, and LoyaltyAccount models."""
from datetime import date
import pytest

from airport_system.domain.passenger import ContactInfo, LoyaltyAccount, Passenger


class TestContactInfo:
    """Tests for ContactInfo class."""

    def test_contact_info_basic(self):
        """Test basic ContactInfo creation."""
        contact = ContactInfo(
            email="test@example.com",
            phone="+1234567890",
            address="123 Main St"
        )
        assert contact.email == "test@example.com"
        assert contact.phone == "+1234567890"
        assert contact.address == "123 Main St"

    def test_is_email_valid_valid_email(self):
        """Test valid email detection."""
        contact = ContactInfo(email="user@example.com", phone="123")
        assert contact.is_email_valid() is True

    def test_is_email_valid_invalid_no_at(self):
        """Test invalid email without @."""
        contact = ContactInfo(email="userexample.com", phone="123")
        assert contact.is_email_valid() is False

    def test_is_email_valid_invalid_no_dot(self):
        """Test invalid email without dot in domain."""
        contact = ContactInfo(email="user@examplecom", phone="123")
        assert contact.is_email_valid() is False

    def test_has_emergency_contact_true(self):
        """Test emergency contact exists."""
        contact = ContactInfo(
            email="test@example.com",
            phone="123",
            emergency_phone="+9999999"
        )
        assert contact.has_emergency_contact() is True

    def test_has_emergency_contact_false(self):
        """Test emergency contact not set."""
        contact = ContactInfo(email="test@example.com", phone="123")
        assert contact.has_emergency_contact() is False

    def test_masked_email_normal(self):
        """Test masking normal email."""
        contact = ContactInfo(email="johndoe@example.com", phone="123")
        masked = contact.masked_email()
        assert masked.startswith("j")
        assert masked.endswith("e@example.com")
        assert "*" in masked

    def test_masked_email_short_name(self):
        """Test masking email with short username (1-2 chars)."""
        contact = ContactInfo(email="ab@example.com", phone="123")
        masked = contact.masked_email()
        assert masked == "**@example.com"

    def test_masked_email_no_at(self):
        """Test masking email without @."""
        contact = ContactInfo(email="invalid", phone="123")
        masked = contact.masked_email()
        assert masked == "invalid"


class TestLoyaltyAccount:
    """Tests for LoyaltyAccount class."""

    def test_loyalty_account_basic(self):
        """Test basic LoyaltyAccount creation."""
        account = LoyaltyAccount(number="L123")
        assert account.number == "L123"
        assert account.points == 0
        assert account.tier == "BRONZE"

    def test_add_points(self):
        """Test adding points."""
        account = LoyaltyAccount(number="L123")
        account.add_points(5000)
        assert account.points == 5000

    def test_add_points_negative_raises(self):
        """Test adding negative points raises error."""
        account = LoyaltyAccount(number="L123")
        with pytest.raises(ValueError, match="Points amount must be positive"):
            account.add_points(-100)

    def test_redeem_points(self):
        """Test redeeming points."""
        account = LoyaltyAccount(number="L123", points=10000)
        account.redeem_points(5000)
        assert account.points == 5000

    def test_redeem_points_negative_raises(self):
        """Test redeeming negative points raises error."""
        account = LoyaltyAccount(number="L123", points=10000)
        with pytest.raises(ValueError, match="Points amount must be positive"):
            account.redeem_points(-100)

    def test_redeem_points_not_enough_raises(self):
        """Test redeeming more than available raises error."""
        account = LoyaltyAccount(number="L123", points=100)
        with pytest.raises(ValueError, match="Not enough points"):
            account.redeem_points(200)

    def test_tier_recalculation_silver(self):
        """Test tier recalculation to Silver."""
        account = LoyaltyAccount(number="L123")
        account.add_points(20000)
        assert account.tier == "SILVER"

    def test_tier_recalculation_gold(self):
        """Test tier recalculation to Gold."""
        account = LoyaltyAccount(number="L123")
        account.add_points(50000)
        assert account.tier == "GOLD"

    def test_tier_recalculation_platinum(self):
        """Test tier recalculation to Platinum."""
        account = LoyaltyAccount(number="L123")
        account.add_points(100000)
        assert account.tier == "PLATINUM"

    def test_tier_downgrade_after_redeem(self):
        """Test tier downgrade after redeeming points."""
        account = LoyaltyAccount(number="L123")
        account.add_points(100000)
        assert account.tier == "PLATINUM"
        account.redeem_points(90000)
        assert account.tier == "BRONZE"

    def test_will_expire_within_no_expiry(self):
        """Test will_expire_within when no expiry date."""
        account = LoyaltyAccount(number="L123")
        assert account.will_expire_within(30) is False

    def test_will_expire_within_soon(self):
        """Test will_expire_within when expiry is soon."""
        from datetime import timedelta
        account = LoyaltyAccount(
            number="L123",
            status_expiry=date.today() + timedelta(days=10)
        )
        assert account.will_expire_within(30) is True
        assert account.will_expire_within(5) is False


class TestPassenger:
    """Tests for Passenger class."""

    def test_passenger_basic(self):
        """Test basic Passenger creation."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact,
            nationality="US"
        )
        assert passenger.passenger_id == "P1"
        assert passenger.name == "John Doe"
        assert passenger.nationality == "US"

    def test_link_loyalty(self):
        """Test linking loyalty account."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        account = LoyaltyAccount(number="L123")
        passenger.link_loyalty(account)
        assert passenger.loyalty is account

    def test_add_note(self):
        """Test adding notes to passenger."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        passenger.add_note("VIP treatment")
        passenger.add_note("Wheelchair assistance")
        assert len(passenger.notes) == 2
        assert "VIP treatment" in passenger.notes

    def test_mark_security_cleared(self):
        """Test marking security cleared."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        assert passenger.security_cleared is False
        passenger.mark_security_cleared()
        assert passenger.security_cleared is True

    def test_can_board_not_cleared(self):
        """Test can_board when not security cleared."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        assert passenger.can_board() is False

    def test_can_board_cleared(self):
        """Test can_board when security cleared."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        passenger.mark_security_cleared()
        assert passenger.can_board() is True

    def test_update_contact_valid(self):
        """Test updating contact with valid email."""
        contact = ContactInfo(email="old@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        new_contact = ContactInfo(email="new@example.com", phone="456")
        passenger.update_contact(new_contact)
        assert passenger.contact.email == "new@example.com"

    def test_update_contact_invalid_email(self):
        """Test updating contact with invalid email raises."""
        contact = ContactInfo(email="old@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        new_contact = ContactInfo(email="invalid", phone="456")
        with pytest.raises(ValueError, match="Invalid email"):
            passenger.update_contact(new_contact)

    def test_set_and_verify_password(self):
        """Test setting and verifying password."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        passenger.set_password("mypassword")
        assert passenger.verify_password("mypassword") is True
        assert passenger.verify_password("wrong") is False

    def test_age_with_dob(self):
        """Test calculating age with date of birth."""
        contact = ContactInfo(email="test@example.com", phone="123")
        # Person born 30 years ago
        dob = date.today().replace(year=date.today().year - 30)
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact,
            date_of_birth=dob
        )
        assert passenger.age() == 30

    def test_age_without_dob(self):
        """Test age returns None without date of birth."""
        contact = ContactInfo(email="test@example.com", phone="123")
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact
        )
        assert passenger.age() is None

    def test_age_birthday_not_yet(self):
        """Test age when birthday hasn't occurred yet this year."""
        from datetime import timedelta
        contact = ContactInfo(email="test@example.com", phone="123")
        # Birthday is tomorrow
        dob = (date.today() + timedelta(days=1)).replace(year=date.today().year - 30)
        passenger = Passenger(
            passenger_id="P1",
            name="John Doe",
            contact=contact,
            date_of_birth=dob
        )
        assert passenger.age() == 29
