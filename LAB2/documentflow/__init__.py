"""documentflow package: учебно-практический проект документооборота."""

# Import from new structure for backward compatibility
from .core import (
    BaseEntity, IdentifiableMixin, TimestampMixin,
    Validatable, Approvable, Signable, Storable,
    NotifierProtocol, PaymentProcessorProtocol,
    DocumentLike, DocumentRepositoryProtocol
)

from .domain import (
    # Documents
    Document, DocumentMetadata, DocumentAttachment, DocumentVersion,
    Signature, DigitalCertificate, DocumentHistoryRecord, DocumentLock,
    IncomingDocument, OutgoingDocument, ContractDocument, InvoiceDocument,
    OrderDocument, DocumentRegistry,
    # Users
    User, Role, Permission, Department, Organization, AccessPolicy,
    # Workflow
    WorkflowState, ApprovalStep, ApprovalTask, ApprovalRoute,
    WorkflowTransition, Notification,
    # Payments
    Currency, Account, Transaction, PaymentOrder, BalanceChecker,
    # Security
    PasswordPolicy, Session, Token, QuotaManager
)

from .services import (
    DocumentService, ValidationService,
    NotificationService, ConsoleNotifier,
    ApprovalService, PaymentService,
    AuthService, SearchService
)

from .infrastructure import (
    DocumentStorage, StorageLocation, ArchiveService,
    InMemoryDocumentRepository, InMemoryPaymentProcessor
)

from . import exceptions

__all__ = [
    # Core
    "BaseEntity", "IdentifiableMixin", "TimestampMixin",
    "Validatable", "Approvable", "Signable", "Storable",
    "NotifierProtocol", "PaymentProcessorProtocol",
    "DocumentLike", "DocumentRepositoryProtocol",
    # Domain - Documents
    "Document", "DocumentMetadata", "DocumentAttachment", "DocumentVersion",
    "Signature", "DigitalCertificate", "DocumentHistoryRecord", "DocumentLock",
    "IncomingDocument", "OutgoingDocument", "ContractDocument", "InvoiceDocument",
    "OrderDocument", "DocumentRegistry",
    # Domain - Users
    "User", "Role", "Permission", "Department", "Organization", "AccessPolicy",
    # Domain - Workflow
    "WorkflowState", "ApprovalStep", "ApprovalTask", "ApprovalRoute",
    "WorkflowTransition", "Notification",
    # Domain - Payments
    "Currency", "Account", "Transaction", "PaymentOrder", "BalanceChecker",
    # Domain - Security
    "PasswordPolicy", "Session", "Token", "QuotaManager",
    # Services
    "DocumentService", "ValidationService",
    "NotificationService", "ConsoleNotifier",
    "ApprovalService", "PaymentService",
    "AuthService", "SearchService",
    # Infrastructure
    "DocumentStorage", "StorageLocation", "ArchiveService",
    "InMemoryDocumentRepository", "InMemoryPaymentProcessor",
    # Exceptions
    "exceptions",
]

