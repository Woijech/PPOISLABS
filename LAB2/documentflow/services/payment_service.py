"""Payment processing services."""

from dataclasses import dataclass
from ..core import PaymentProcessorProtocol
from ..domain import InvoiceDocument
from .notification_service import NotificationService


@dataclass
class PaymentService:
    """Service for processing payments."""
    
    processor: PaymentProcessorProtocol
    notifier: NotificationService
    
    def pay_invoice(self, invoice: InvoiceDocument, src: str, dst: str, amount: int) -> str:
        """Process payment for an invoice."""
        tx = self.processor.transfer(src, dst, amount)
        invoice.mark_paid()
        self.notifier.send(f"Оплата счёта {invoice.number} проведена: {tx}")
        return tx
