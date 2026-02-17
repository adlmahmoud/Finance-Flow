"""
Analytics and Reporting Service.
Handles data analysis, statistics, and financial insights.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sqlmodel import Session, select, func

from loguru import logger
from models.database import (
    Transaction,
    TransactionType,
    TransactionCategory,
    BankAccount,
    Budget,
)


class AnalyticsService:
    """Service for financial analytics and insights."""

    def __init__(self, session: Session):
        """
        Initialize analytics service.
        
        Args:
            session: Database session
        """
        self.session = session

    def get_total_balance(self, user_id: int) -> float:
        """
        Get total balance across all accounts.
        
        Args:
            user_id: User ID
            
        Returns:
            Total balance
        """
        query = select(func.sum(BankAccount.balance)).where(
            BankAccount.user_id == user_id
        )
        result = self.session.exec(query).first()
        return float(result or 0)

    def get_account_balance(self, account_id: int) -> float:
        """Get balance for a specific account."""
        account = self.session.get(BankAccount, account_id)
        return account.balance if account else 0.0

    def get_monthly_balance_trend(
        self,
        user_id: int,
        months_back: int = 12,
    ) -> List[Dict[str, any]]:
        """
        Get balance trend over months.
        
        Args:
            user_id: User ID
            months_back: Number of months to include
            
        Returns:
            List of monthly data with date, income, expenses, and net
        """
        trends = []
        
        for i in range(months_back, 0, -1):
            current_date = datetime.utcnow()
            month_date = current_date - timedelta(days=current_date.day - 1)
            month_date = month_date - timedelta(days=30 * i)

            year = month_date.year
            month = month_date.month

            # Get all accounts for user
            accounts_query = select(BankAccount).where(BankAccount.user_id == user_id)
            accounts = self.session.exec(accounts_query).all()
            account_ids = [acc.id for acc in accounts]

            if not account_ids:
                continue

            # Calculate monthly totals
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            txn_query = (
                select(Transaction.transaction_type, func.sum(Transaction.amount))
                .where(Transaction.account_id.in_(account_ids))
                .where(Transaction.date >= start_date)
                .where(Transaction.date < end_date)
                .group_by(Transaction.transaction_type)
            )

            results = self.session.exec(txn_query).all()

            income = 0.0
            expenses = 0.0
            for txn_type, total in results:
                if txn_type == TransactionType.INCOME:
                    income = float(total or 0)
                elif txn_type == TransactionType.EXPENSE:
                    expenses = float(total or 0)

            trends.append({
                "date": start_date.strftime("%Y-%m"),
                "income": income,
                "expenses": expenses,
                "net": income - expenses,
            })

        return trends

    def get_spending_by_category(
        self,
        user_id: int,
        days_back: int = 30,
    ) -> Dict[str, float]:
        """
        Get spending breakdown by category.
        
        Args:
            user_id: User ID
            days_back: Number of days to analyze
            
        Returns:
            Dictionary mapping category name to spent amount
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)

        # Get all accounts for user
        accounts_query = select(BankAccount).where(BankAccount.user_id == user_id)
        accounts = self.session.exec(accounts_query).all()
        account_ids = [acc.id for acc in accounts]

        if not account_ids:
            return {}

        query = (
            select(Transaction.category, func.sum(Transaction.amount))
            .where(Transaction.account_id.in_(account_ids))
            .where(Transaction.transaction_type == TransactionType.EXPENSE)
            .where(Transaction.date >= start_date)
            .group_by(Transaction.category)
        )

        results = self.session.exec(query).all()

        return {
            category.value: float(amount or 0)
            for category, amount in results
        }

    def get_budget_status(self, user_id: int) -> List[Dict[str, any]]:
        """
        Get budget status for all categories.
        
        Args:
            user_id: User ID
            
        Returns:
            List of budget status by category
        """
        budgets_query = select(Budget).where(Budget.user_id == user_id)
        budgets = self.session.exec(budgets_query).all()

        # Get current month spending
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)

        # Get all accounts for user
        accounts_query = select(BankAccount).where(BankAccount.user_id == user_id)
        accounts = self.session.exec(accounts_query).all()
        account_ids = [acc.id for acc in accounts]

        budget_status = []
        
        for budget in budgets:
            # Get spending for this category this month
            spending_query = (
                select(func.sum(Transaction.amount))
                .where(Transaction.account_id.in_(account_ids))
                .where(Transaction.category == budget.category)
                .where(Transaction.transaction_type == TransactionType.EXPENSE)
                .where(Transaction.date >= start_of_month)
            )

            spent = float(self.session.exec(spending_query).first() or 0)
            remaining = budget.monthly_limit - spent
            percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0

            budget_status.append({
                "category": budget.category.value,
                "limit": budget.monthly_limit,
                "spent": spent,
                "remaining": max(0, remaining),
                "percentage": min(100, max(0, percentage)),
                "exceeded": spent > budget.monthly_limit,
            })

        return budget_status

    def get_insights(self, user_id: int) -> Dict[str, any]:
        """
        Generate financial insights and recommendations.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with various insights
        """
        # Get 3 months of data
        spending_by_category = self.get_spending_by_category(user_id, days_back=90)
        balance_trend = self.get_monthly_balance_trend(user_id, months_back=3)
        budget_status = self.get_budget_status(user_id)

        # Calculate averages
        avg_monthly_expense = sum(
            item["expenses"]
            for item in balance_trend
        ) / len(balance_trend) if balance_trend else 0

        # Identify top spending categories
        top_categories = sorted(
            spending_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        # Check budget alerts
        budget_alerts = [b for b in budget_status if b["exceeded"]]

        insights = {
            "total_balance": self.get_total_balance(user_id),
            "average_monthly_expense": round(avg_monthly_expense, 2),
            "top_categories": [
                {"category": cat, "amount": round(amount, 2)}
                for cat, amount in top_categories
            ],
            "budget_alerts": budget_alerts,
            "recommendation": self._generate_recommendation(
                avg_monthly_expense,
                budget_alerts,
                spending_by_category,
            ),
        }

        return insights

    @staticmethod
    def _generate_recommendation(
        avg_expense: float,
        budget_alerts: List[Dict],
        spending: Dict[str, float],
    ) -> str:
        """Generate financial recommendation based on data."""
        if budget_alerts:
            return f"⚠️ Vous avez dépassé votre budget dans {len(budget_alerts)} catégorie(s). Réduisez vos dépenses."
        
        if avg_expense > 3000:
            return f"💡 Vos dépenses moyennes ({avg_expense:.0f}€) sont élevées. Analysez les grandes dépenses."
        
        high_expense_category = max(spending.items(), key=lambda x: x[1], default=("", 0))
        if high_expense_category[1] > 500:
            return f"💡 Le {high_expense_category[0]} représente une dépense importante. Pouvez-vous économiser?"
        
        return "✅ Vos finances semblent en bon état!"

    def export_monthly_report(
        self,
        user_id: int,
        year: int,
        month: int,
    ) -> Dict[str, any]:
        """
        Generate a complete monthly financial report.
        
        Args:
            user_id: User ID
            year: Year
            month: Month
            
        Returns:
            Complete monthly report
        """
        # Get all accounts
        accounts_query = select(BankAccount).where(BankAccount.user_id == user_id)
        accounts = self.session.exec(accounts_query).all()
        account_ids = [acc.id for acc in accounts]

        if not account_ids:
            return {}

        # Date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # Get transactions
        txn_query = (
            select(Transaction)
            .where(Transaction.account_id.in_(account_ids))
            .where(Transaction.date >= start_date)
            .where(Transaction.date < end_date)
            .order_by(Transaction.date.desc())
        )

        transactions = self.session.exec(txn_query).all()

        # Calculate totals
        income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
        expenses = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)

        # Get category breakdown
        category_spending = {}
        for txn in transactions:
            if txn.transaction_type == TransactionType.EXPENSE:
                category_spending[txn.category.value] = (
                    category_spending.get(txn.category.value, 0) + txn.amount
                )

        return {
            "period": f"{year}-{month:02d}",
            "total_income": round(income, 2),
            "total_expenses": round(expenses, 2),
            "net_balance": round(income - expenses, 2),
            "category_breakdown": {k: round(v, 2) for k, v in category_spending.items()},
            "transaction_count": len(transactions),
            "accounts": [{"id": acc.id, "name": acc.account_name} for acc in accounts],
        }
