"""Payment processor implementations."""

from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
from ..domain import Account, Transaction, BalanceChecker


@dataclass
class InMemoryPaymentProcessor:
    """In-memory payment processor implementation."""
    
    accounts: Dict[str, Account]
    balance_checker: BalanceChecker
    transactions: List[Transaction] = field(default_factory=list)
    daily_limit: int = 1000000
    
    def transfer(self, src_account: str, dst_account: str, amount: int) -> str:
        """Transfer money between accounts."""
        src = self.accounts[src_account]
        dst = self.accounts[dst_account]
        self.balance_checker.ensure_same_currency(src, dst)
        src.debit(amount)
        dst.credit(amount)
        tx_id = f"tx-{len(self.transactions)+1}"
        self.transactions.append(
            Transaction(
                id=tx_id, 
                src=src_account, 
                dst=dst_account, 
                amount=amount, 
                created_at=datetime.utcnow()
            )
        )
        return tx_id
    
    def get_account_balance(self, account_number: str) -> int:
        """Get account balance"""
        return self.accounts[account_number].balance
    
    def get_transaction_history(self, account_number: str) -> List[Transaction]:
        """Get transaction history for account"""
        return [tx for tx in self.transactions if tx.src == account_number or tx.dst == account_number]
    
    def check_daily_limit(self, amount: int) -> bool:
        """Check if amount is within daily limit"""
        return amount <= self.daily_limit
