"""Document search services."""

from dataclasses import dataclass
from typing import List
from ..core import DocumentRepositoryProtocol
from ..domain import Document


@dataclass
class SearchService:
    """Service for searching documents."""
    
    repo: DocumentRepositoryProtocol
    
    def find(self, query: str) -> List[Document]:
        """Search for documents matching the query."""
        return list(self.repo.search(query))
