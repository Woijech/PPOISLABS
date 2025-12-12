"""Notification services for documentflow system."""

from dataclasses import dataclass
from ..core import NotifierProtocol


@dataclass
class ConsoleNotifier(NotifierProtocol):
    """Console-based notification implementation."""
    
    def notify(self, message: str) -> None:
        """Print notification to console."""
        print(f"[NOTIFY] {message}")


@dataclass
class NotificationService:
    """Service for sending notifications through various channels."""
    
    notifier: NotifierProtocol
    
    def send(self, message: str) -> None:
        """Send a notification message."""
        self.notifier.notify(message)
