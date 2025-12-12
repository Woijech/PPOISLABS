"""Storage infrastructure for documents."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
from ..exceptions import DocumentNotFoundError
from ..domain import Document, DocumentAttachment, QuotaManager, WorkflowState


@dataclass
class StorageLocation:
    """Represents a storage location for documents."""
    
    name: str
    base_path: str
    is_active: bool = True
    capacity: int = 0
    
    def validate_path(self) -> bool:
        """Validate that path is not empty"""
        return bool(self.base_path)
    
    def get_full_path(self, filename: str) -> str:
        """Get full path to file"""
        return f"{self.base_path}/{filename}"


@dataclass
class DocumentStorage:
    """Storage system for documents and attachments."""
    
    location: StorageLocation
    quota: QuotaManager
    _docs: Dict[str, Document] = field(default_factory=dict)
    _attachments: Dict[str, DocumentAttachment] = field(default_factory=dict)

    def save(self, doc: Document) -> None:
        """Save a document to storage."""
        self._docs[doc.number] = doc

    def get(self, number: str) -> Document:
        """Retrieve a document by number."""
        try:
            return self._docs[number]
        except KeyError as e:
            raise DocumentNotFoundError(number) from e

    def exists(self, number: str) -> bool:
        """Check if a document exists in storage."""
        return number in self._docs

    def store_attachment(self, doc: Document, att: DocumentAttachment) -> None:
        """Store a document attachment."""
        # allocate() will raise exception if quota is exceeded
        self.quota.allocate(att.size)
        self._attachments[f"{doc.number}:{att.filename}"] = att

    def archive(self, doc: Document) -> None:
        """Archive a document."""
        doc.archive()
    
    def delete(self, number: str) -> None:
        """Delete document from storage"""
        if number in self._docs:
            del self._docs[number]
    
    def count_documents(self) -> int:
        """Count total documents in storage"""
        return len(self._docs)
    
    def get_all_numbers(self) -> List[str]:
        """Get all document numbers"""
        return list(self._docs.keys())
    
    def clear(self) -> None:
        """Clear all documents from storage"""
        self._docs.clear()
        self._attachments.clear()


@dataclass
class ArchiveService:
    """Service for managing archived documents."""
    
    storage: DocumentStorage
    archive_retention_days: int = 365
    
    def archive_document(self, number: str) -> None:
        """Archive a document by number."""
        doc = self.storage.get(number)
        self.storage.archive(doc)
    
    def restore_document(self, number: str) -> None:
        """Restore an archived document."""
        doc = self.storage.get(number)
        doc.restore()
    
    def get_archived_documents(self) -> List[Document]:
        """Get all archived documents"""
        return [doc for doc in self.storage._docs.values() if doc.status == WorkflowState.ARCHIVED]
    
    def can_delete_archived(self, doc: Document) -> bool:
        """Check if archived document can be permanently deleted"""
        if doc.status != WorkflowState.ARCHIVED:
            return False
        age_days = (datetime.utcnow() - doc.created_at).days
        return age_days > self.archive_retention_days
