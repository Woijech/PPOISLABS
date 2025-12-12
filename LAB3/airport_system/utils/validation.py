from __future__ import annotations


def ensure_not_empty(value: str, field_name: str) -> None:
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def ensure_positive(number: float, field_name: str) -> None:
    if number <= 0:
        raise ValueError(f"{field_name} must be positive")
