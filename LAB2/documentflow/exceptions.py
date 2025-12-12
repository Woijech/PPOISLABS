"""Custom exceptions for documentflow system."""


class DocumentFlowError(Exception):
    """Base exception for all documentflow errors."""
    
    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(self.message)


class DocumentNotFoundError(DocumentFlowError):
    """Raised when a document is not found in the system."""
    
    def __init__(self, document_id: str = ""):
        message = f"Document not found: {document_id}" if document_id else "Document not found"
        super().__init__(message)


class InvalidDocumentStatusError(DocumentFlowError):
    """Raised when attempting an operation on a document with invalid status."""
    
    def __init__(self, message: str = "Invalid document status"):
        super().__init__(message)


class AccessDeniedError(DocumentFlowError):
    """Raised when user lacks permissions for an operation."""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message)


class ApprovalStepError(DocumentFlowError):
    """Raised when there's an error in approval workflow processing."""
    
    def __init__(self, message: str = "Approval step error"):
        super().__init__(message)


class InvalidSignatureError(DocumentFlowError):
    """Raised when a document signature is invalid or missing."""
    
    def __init__(self, message: str = "Invalid signature"):
        super().__init__(message)


class UserBlockedError(DocumentFlowError):
    """Raised when attempting operations with a blocked user."""
    
    def __init__(self, user_id: str = ""):
        message = f"User is blocked: {user_id}" if user_id else "User is blocked"
        super().__init__(message)


class VersionConflictError(DocumentFlowError):
    """Raised when there's a version conflict during document operations."""
    
    def __init__(self, message: str = "Version conflict detected"):
        super().__init__(message)


class RouteNotFoundError(DocumentFlowError):
    """Raised when an approval route is not found."""
    
    def __init__(self, route_id: str = ""):
        message = f"Approval route not found: {route_id}" if route_id else "Approval route not found"
        super().__init__(message)


class PaymentOperationError(DocumentFlowError):
    """Raised when a payment operation fails."""
    
    def __init__(self, message: str = "Payment operation failed"):
        super().__init__(message)


class AuthFailedError(DocumentFlowError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class DuplicateDocumentError(DocumentFlowError):
    """Raised when attempting to register a document with duplicate number."""
    
    def __init__(self, message: str = "Duplicate document number"):
        super().__init__(message)


class StorageLimitExceededError(DocumentFlowError):
    """Raised when storage quota or limit is exceeded."""
    
    def __init__(self, message: str = "Storage limit exceeded"):
        super().__init__(message)
