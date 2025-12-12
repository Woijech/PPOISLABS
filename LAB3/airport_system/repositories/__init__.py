"""
Simple in-memory repositories for domain objects.
"""
from .base import InMemoryRepository
from .booking_repository import BookingRepository
from .flight_repository import FlightRepository

__all__ = ["InMemoryRepository", "BookingRepository", "FlightRepository"]
