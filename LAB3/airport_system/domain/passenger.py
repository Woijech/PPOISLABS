from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class ContactInfo:
    email: str
    phone: str
    address: str = ""
    emergency_phone: Optional[str] = None

    def is_email_valid(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[-1]

    def has_emergency_contact(self) -> bool:
        return bool(self.emergency_phone)

    def masked_email(self) -> str:
        if "@" not in self.email:
            return self.email
        name, domain = self.email.split("@", 1)
        if len(name) <= 2:
            return "*" * len(name) + "@" + domain
        return name[0] + "*" * (len(name) - 2) + name[-1] + "@" + domain


@dataclass
class LoyaltyAccount:
    number: str
    points: int = 0
    tier: str = "BRONZE"
    status_expiry: Optional[date] = None

    def add_points(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Points amount must be positive")
        self.points += amount
        self._recalculate_tier()

    def redeem_points(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Points amount must be positive")
        if amount > self.points:
            raise ValueError("Not enough points")
        self.points -= amount
        self._recalculate_tier()

    def _recalculate_tier(self) -> None:
        if self.points >= 100000:
            self.tier = "PLATINUM"
        elif self.points >= 50000:
            self.tier = "GOLD"
        elif self.points >= 20000:
            self.tier = "SILVER"
        else:
            self.tier = "BRONZE"

    def will_expire_within(self, days: int) -> bool:
        if not self.status_expiry:
            return False
        return (self.status_expiry - date.today()).days <= days


@dataclass
class Passenger:
    passenger_id: str
    name: str
    contact: ContactInfo
    loyalty: Optional[LoyaltyAccount] = None
    is_vip: bool = False
    security_cleared: bool = False
    notes: List[str] = field(default_factory=list)
    passport_number: str = ""
    nationality: str = ""
    date_of_birth: Optional[date] = None
    password_hash: str = ""

    def link_loyalty(self, account: LoyaltyAccount) -> None:
        self.loyalty = account

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def mark_security_cleared(self) -> None:
        self.security_cleared = True

    def can_board(self) -> bool:
        return self.security_cleared

    def update_contact(self, new_contact: ContactInfo) -> None:
        if not new_contact.is_email_valid():
            raise ValueError("Invalid email")
        self.contact = new_contact

    def set_password(self, raw_password: str) -> None:
        # примитивный "хеш" для учебных целей
        self.password_hash = raw_password[::-1]

    def verify_password(self, raw_password: str) -> bool:
        return self.password_hash == raw_password[::-1]

    def age(self) -> Optional[int]:
        if not self.date_of_birth:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years
