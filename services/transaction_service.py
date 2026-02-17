"""
Transaction Management Service.
Handles CRUD operations and business logic for transactions.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func

from loguru import logger
from models.database import (
    Transaction,
    TransactionCategory,
    TransactionType,
    BankAccount,
    Budget,
)


class TransactionService:
    """Service for transaction management."""

    def __init__(self, session: Session):
        """
        Initialize transaction service.
        
        Args:
            session: Database session
        """
        self.session = session

    def create_transaction(self, transaction: Transaction) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction: Transaction object to create
            
        Returns:
            Created transaction with ID
        """
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        logger.info(f"Transaction created: {transaction.id}")
        return transaction

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return self.session.get(Transaction, transaction_id)

    def get_transactions_for_account(
        self,
        account_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Transaction]:
        """
        Get transactions for an account with optional date range.
        
        Args:
            account_id: Bank account ID
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of transactions
        """
        query = select(Transaction).where(Transaction.account_id == account_id)
        
        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        
        query = query.order_by(Transaction.date.desc())
        return self.session.exec(query).all()

    def get_transactions_by_category(
        self,
        account_id: int,
        category: TransactionCategory,
        days_back: int = 30,
    ) -> List[Transaction]:
        """Get transactions by category."""
        start_date = datetime.utcnow() - timedelta(days=days_back)
        query = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .where(Transaction.category == category)
            .where(Transaction.date >= start_date)
            .order_by(Transaction.date.desc())
        )
        return self.session.exec(query).all()

    def update_transaction(self, transaction_id: int, **kwargs) -> Optional[Transaction]:
        """Update transaction fields."""
        transaction = self.get_transaction(transaction_id)
        if transaction:
            for key, value in kwargs.items():
                setattr(transaction, key, value)
            transaction.updated_at = datetime.utcnow()
            self.session.add(transaction)
            self.session.commit()
            self.session.refresh(transaction)
            logger.info(f"Transaction {transaction_id} updated")
        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction."""
        transaction = self.get_transaction(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            logger.info(f"Transaction {transaction_id} deleted")
            return True
        return False

    def import_transactions_from_bank(
        self,
        account_id: int,
        bank_transactions: List[Dict[str, Any]],
    ) -> List[Transaction]:
        """
        Import transactions from bank API.
        
        Args:
            account_id: Bank account ID
            bank_transactions: List of transaction dicts from bank API
            
        Returns:
            List of created transactions
        """
        created_transactions = []
        
        for bank_txn in bank_transactions:
            # Check if transaction already exists (by external_id)
            if bank_txn.get("external_id"):
                existing = self.session.exec(
                    select(Transaction).where(
                        Transaction.external_id == bank_txn["external_id"]
                    )
                ).first()
                
                if existing:
                    logger.debug(f"Transaction {bank_txn['external_id']} already exists")
                    continue

            # Create new transaction
            transaction = Transaction(
                account_id=account_id,
                description=bank_txn.get("description", ""),
                merchant=bank_txn.get("merchant"),
                amount=bank_txn.get("amount", 0),
                category=bank_txn.get("category", TransactionCategory.OTHER),
                transaction_type=bank_txn.get("transaction_type", TransactionType.EXPENSE),
                external_id=bank_txn.get("external_id"),
                date=datetime.fromisoformat(bank_txn["date"]),
            )
            
            self.session.add(transaction)
            created_transactions.append(transaction)

        if created_transactions:
            self.session.commit()
            logger.info(f"Imported {len(created_transactions)} transactions")

        return created_transactions

    def get_monthly_summary(
        self,
        account_id: int,
        year: int,
        month: int,
    ) -> Dict[str, float]:
        """
        Get monthly summary for an account.
        
        Args:
            account_id: Bank account ID
            year: Year
            month: Month (1-12)
            
        Returns:
            Dictionary with income, expenses, and net
        """
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        query = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .where(Transaction.date >= start_date)
            .where(Transaction.date < end_date)
        )
        
        transactions = self.session.exec(query).all()

        income = sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.INCOME
        )
        expenses = sum(
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.EXPENSE
        )

        return {
            "income": income,
            "expenses": expenses,
            "net": income - expenses,
        }

    def get_category_spending(
        self,
        account_id: int,
        days_back: int = 30,
    ) -> Dict[TransactionCategory, float]:
        """
        Get spending by category.
        
        Args:
            account_id: Bank account ID
            days_back: Number of days to include
            
        Returns:
            Dictionary mapping category to total spent
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)
        query = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .where(Transaction.transaction_type == TransactionType.EXPENSE)
            .where(Transaction.date >= start_date)
        )
        
        transactions = self.session.exec(query).all()
        
        spending: Dict[TransactionCategory, float] = {}
        for txn in transactions:
            spending[txn.category] = spending.get(txn.category, 0) + txn.amount

        return spending
