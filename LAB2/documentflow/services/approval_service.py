"""Approval workflow services."""

from dataclasses import dataclass
from ..domain import ApprovalRoute, ApprovalStep, Document
from .notification_service import NotificationService


@dataclass
class ApprovalService:
    """Service for managing document approvals."""
    
    notifier: NotificationService
    
    def route_for_role(self, role_name: str) -> ApprovalRoute:
        """Create a simple approval route for a given role."""
        steps = [ApprovalStep(name="Проверка", role_name=role_name)]
        return ApprovalRoute(name=f"route:{role_name}", steps=steps)
    
    def approve(self, doc: Document) -> None:
        """Approve a document."""
        doc.approve()
        self.notifier.send(f"Документ согласован: {doc.number}")
