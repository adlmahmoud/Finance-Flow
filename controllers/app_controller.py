"""
Application Controller - Business Logic Layer.
Orchestrates services and handles application workflow.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlmodel import Session

from loguru import logger
from models.database import (
    User,
    BankAccount,
    Transaction,
    Budget,
    TransactionCategory,
)
from models.database_init import DatabaseManager
from services.bank_service import BankServiceFactory
from services.transaction_service import TransactionService
from services.analytics_service import AnalyticsService
from utils.security import SecurityManager


class AppController:
    """Main application controller handling business logic."""

    def __init__(self):
        """Initialize controller and services."""
        self.db = DatabaseManager.init_db()
        self.bank_service = BankServiceFactory.create()
        self.security = SecurityManager()
        self.current_user: Optional[User] = None
        logger.info("AppController initialized")

    def _get_session(self) -> Session:
        """Get a database session."""
        return DatabaseManager.get_session()

    # ===================== User Management =====================

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        monthly_budget: float = 3000.0,
    ) -> User:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            password: Password (will be hashed)
            full_name: Full name
            monthly_budget: Monthly budget limit
            
        Returns:
            Created user
        """
        session = self._get_session()
        try:
            # Hash password
            password_hash = self.security.hash_password(password)

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                full_name=full_name,
                monthly_budget=monthly_budget,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"User created: {username}")
            return user
        finally:
            DatabaseManager.close_session(session)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            User if authenticated, None otherwise
        """
        session = self._get_session()
        try:
            from sqlmodel import select

            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()

            if user and self.security.verify_password(password, user.password_hash):
                self.current_user = user
                logger.info(f"User authenticated: {username}")
                return user

            logger.warning(f"Authentication failed for: {username}")
            return None
        finally:
            DatabaseManager.close_session(session)

    # ===================== Bank Account Management =====================

    def add_bank_account(
        self,
        user_id: int,
        account_name: str,
        account_number: str,
        bank_name: str,
    ) -> BankAccount:
        """
        Add a new bank account for user.
        
        Args:
            user_id: User ID
            account_name: Account name
            account_number: Account number
            bank_name: Bank name
            
        Returns:
            Created bank account
        """
        session = self._get_session()
        try:
            account = BankAccount(
                user_id=user_id,
                account_name=account_name,
                account_number=account_number,
                bank_name=bank_name,
                balance=0.0,
            )
            session.add(account)
            session.commit()
            session.refresh(account)
            logger.info(f"Bank account created: {account_name}")
            return account
        finally:
            DatabaseManager.close_session(session)

    def get_user_accounts(self, user_id: int) -> List[BankAccount]:
        """Get all accounts for a user."""
        session = self._get_session()
        try:
            from sqlmodel import select

            statement = select(BankAccount).where(BankAccount.user_id == user_id)
            return session.exec(statement).all()
        finally:
            DatabaseManager.close_session(session)

    # ===================== Transaction Sync =====================

    def sync_transactions_from_bank(self, user_id: int) -> Dict[int, int]:
        """
        Sync transactions from bank service for all user accounts.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary mapping account_id to number of transactions imported
        """
        session = self._get_session()
        try:
            accounts = self.get_user_accounts(user_id)
            transaction_service = TransactionService(session)
            results = {}

            for account in accounts:
                # Get transactions from bank
                bank_txns = self.bank_service.get_transactions(account.bank_api_id or account.id)

                # Import transactions
                imported = transaction_service.import_transactions_from_bank(
                    account.id,
                    bank_txns,
                )
                results[account.id] = len(imported)

            logger.info(f"Synced transactions for user {user_id}: {results}")
            return results
        finally:
            DatabaseManager.close_session(session)

    # ===================== Transaction Management =====================

    def get_transactions(
        self,
        user_id: int,
        account_id: Optional[int] = None,
        days_back: int = 30,
    ) -> List[Transaction]:
        """
        Get transactions for user or specific account.
        
        Args:
            user_id: User ID
            account_id: Optional account ID (if None, get all user accounts)
            days_back: Number of days to include
            
        Returns:
            List of transactions
        """
        session = self._get_session()
        try:
            from sqlmodel import select
            from datetime import timedelta

            start_date = datetime.utcnow() - timedelta(days=days_back)

            if account_id:
                query = (
                    select(Transaction)
                    .where(Transaction.account_id == account_id)
                    .where(Transaction.date >= start_date)
                    .order_by(Transaction.date.desc())
                )
            else:
                # Get all accounts for user
                accounts = self.get_user_accounts(user_id)
                account_ids = [acc.id for acc in accounts]

                if not account_ids:
                    return []

                query = (
                    select(Transaction)
                    .where(Transaction.account_id.in_(account_ids))
                    .where(Transaction.date >= start_date)
                    .order_by(Transaction.date.desc())
                )

            return session.exec(query).all()
        finally:
            DatabaseManager.close_session(session)

    # ===================== Budget Management =====================

    def set_category_budget(
        self,
        user_id: int,
        category: TransactionCategory,
        monthly_limit: float,
    ) -> Budget:
        """
        Set budget for a category.
        
        Args:
            user_id: User ID
            category: Transaction category
            monthly_limit: Monthly spending limit
            
        Returns:
            Created/updated budget
        """
        session = self._get_session()
        try:
            from sqlmodel import select

            # Check if budget exists
            query = (
                select(Budget)
                .where(Budget.user_id == user_id)
                .where(Budget.category == category)
            )
            budget = session.exec(query).first()

            if budget:
                budget.monthly_limit = monthly_limit
            else:
                budget = Budget(
                    user_id=user_id,
                    category=category,
                    monthly_limit=monthly_limit,
                )

            session.add(budget)
            session.commit()
            session.refresh(budget)
            logger.info(f"Budget set for {category}: {monthly_limit}€")
            return budget
        finally:
            DatabaseManager.close_session(session)

    # ===================== Analytics & Reporting =====================

    def get_dashboard_data(self, user_id: int) -> Dict[str, Any]:
        """
        Get all data needed for dashboard.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with dashboard data
        """
        session = self._get_session()
        try:
            analytics = AnalyticsService(session)

            return {
                "total_balance": analytics.get_total_balance(user_id),
                "insights": analytics.get_insights(user_id),
                "spending_by_category": analytics.get_spending_by_category(user_id),
                "budget_status": analytics.get_budget_status(user_id),
                "balance_trend": analytics.get_monthly_balance_trend(user_id, months_back=6),
            }
        finally:
            DatabaseManager.close_session(session)

    def get_monthly_report(self, user_id: int, year: int, month: int) -> Dict[str, Any]:
        """
        Get monthly financial report.
        
        Args:
            user_id: User ID
            year: Year
            month: Month
            
        Returns:
            Monthly report
        """
        session = self._get_session()
        try:
            analytics = AnalyticsService(session)
            return analytics.export_monthly_report(user_id, year, month)
        finally:
            DatabaseManager.close_session(session)

    def get_category_analysis(
        self,
        user_id: int,
        days_back: int = 30,
    ) -> Dict[str, Any]:
        """
        Get detailed category analysis.
        
        Args:
            user_id: User ID
            days_back: Number of days to analyze
            
        Returns:
            Category analysis with charts data
        """
        session = self._get_session()
        try:
            analytics = AnalyticsService(session)
            spending = analytics.get_spending_by_category(user_id, days_back)

            # Create chart data
            chart_data = [
                {"category": cat, "amount": round(amount, 2)}
                for cat, amount in sorted(spending.items(), key=lambda x: x[1], reverse=True)
            ]

            return {
                "total_spent": sum(amount for amount in spending.values()),
                "categories": chart_data,
                "period_days": days_back,
            }
        finally:
            DatabaseManager.close_session(session)
