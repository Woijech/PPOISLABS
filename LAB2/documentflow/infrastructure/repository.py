"""Repository implementations for documents."""

from dataclasses import dataclass
from typing import Iterable
from ..core import DocumentRepositoryProtocol
from ..domain import Document
from ..exceptions import DocumentNotFoundError
from .storage import DocumentStorage


@dataclass
class InMemoryDocumentRepository(DocumentRepositoryProtocol):
    """In-memory implementation of document repository."""
    
    storage: DocumentStorage
    
    def save(self, doc: Document) -> None:
        """Save a document to the repository."""
        self.storage.save(doc)
    
    def get(self, number: str) -> Document | None:
        """Get a document by number, returning None if not found."""
        try:
            return self.storage.get(number)
        except DocumentNotFoundError:
            return None
    
    def exists(self, number: str) -> bool:
        """Check if a document exists in the repository."""
        return self.storage.exists(number)
    
    def search(self, query: str) -> Iterable[Document]:
        """Search for documents matching the query."""
        for d in list(self.storage._docs.values()):
            if query.lower() in d.title.lower() or query.lower() in d.number.lower():
                yield d
