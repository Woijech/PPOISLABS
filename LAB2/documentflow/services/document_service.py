"""Document management services."""

from dataclasses import dataclass
from ..core import DocumentRepositoryProtocol
from ..domain import Document, DocumentAttachment, DocumentRegistry, WorkflowState, ApprovalRoute, User
from ..exceptions import DocumentNotFoundError, AccessDeniedError
from .notification_service import NotificationService


@dataclass
class ValidationService:
    """Service for validating documents."""
    
    def validate(self, doc: Document) -> None:
        """Validate a document."""
        doc.validate()


@dataclass
class DocumentService:
    """Main service for document operations."""
    
    repo: DocumentRepositoryProtocol
    registry: DocumentRegistry
    validator: ValidationService
    notifier: NotificationService

    def register(self, doc: Document) -> None:
        """Register a new document in the system."""
        self.registry.register(doc.number)
        self.validator.validate(doc)
        self.repo.save(doc)
        self.notifier.send(f"Документ зарегистрирован: {doc.number}")

    def add_attachment(self, number: str, att: DocumentAttachment) -> None:
        """Add an attachment to a document."""
        doc = self.require(number)
        doc.add_attachment(att)
        self.repo.save(doc)

    def send_for_approval(self, number: str, route: ApprovalRoute) -> None:
        """Send a document for approval."""
        doc = self.require(number)
        doc.approval_route = route
        doc.status = WorkflowState.IN_REVIEW
        self.repo.save(doc)
        self.notifier.send(f"Документ {number} отправлен на согласование")

    def sign(self, number: str, user: User) -> None:
        """Sign a document with user's digital signature."""
        doc = self.require(number)
        if user.is_blocked:
            raise AccessDeniedError("Пользователь заблокирован")
        doc.sign(user.id)
        self.repo.save(doc)

    def archive(self, number: str) -> None:
        """Archive a document."""
        doc = self.require(number)
        doc.archive()
        self.repo.save(doc)

    def require(self, number: str) -> Document:
        """Get a document or raise an error if not found."""
        doc = self.repo.get(number)
        if not doc:
            raise DocumentNotFoundError(number)
        return doc
