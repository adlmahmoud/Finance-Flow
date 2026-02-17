"""
Database models using SQLModel (SQLAlchemy + Pydantic).
Core data structures for the FinanceFlow application.
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class TransactionCategory(str, Enum):
    """Transaction categories."""
    FOOD = "Alimentation"
    TRANSPORT = "Transport"
    UTILITIES = "Services"
    ENTERTAINMENT = "Loisirs"
    SHOPPING = "Shopping"
    HEALTHCARE = "Santé"
    EDUCATION = "Éducation"
    SALARY = "Salaire"
    INVESTMENT = "Investissement"
    OTHER = "Autre"


class TransactionType(str, Enum):
    """Transaction types."""
    INCOME = "Revenu"
    EXPENSE = "Dépense"
    TRANSFER = "Transfert"


class User(SQLModel, table=True):
    """User model."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str  # Encrypted password
    full_name: Optional[str] = None
    monthly_budget: float = Field(default=3000.0)
    currency: str = Field(default="EUR")
    
    # Relationships
    accounts: List["BankAccount"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "monthly_budget": 3000.0,
                "currency": "EUR",
            }
        }


class BankAccount(SQLModel, table=True):
    """Bank account model."""
    __tablename__ = "bank_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    account_name: str
    account_number: str = Field(unique=True)
    bank_name: str
    balance: float = Field(default=0.0)
    currency: str = Field(default="EUR")
    
    # External API reference
    bank_api_id: Optional[str] = None  # ID from Plaid/GoCardless
    
    # Relationships
    user: User = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Transaction(SQLModel, table=True):
    """Transaction model."""
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="bank_accounts.id")
    
    description: str
    amount: float
    category: TransactionCategory
    transaction_type: TransactionType
    
    # Transaction details
    merchant: Optional[str] = None
    external_id: Optional[str] = None  # ID from bank API
    
    # Relationships
    account: BankAccount = Relationship(back_populates="transactions")
    
    date: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Supermarché",
                "amount": 45.50,
                "category": "Alimentation",
                "transaction_type": "Dépense",
                "merchant": "Carrefour",
                "date": "2024-02-15T10:30:00",
            }
        }


class Budget(SQLModel, table=True):
    """Budget model for category-based budgeting."""
    __tablename__ = "budgets"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    category: TransactionCategory
    monthly_limit: float
    spent_this_month: float = Field(default=0.0)
    
    # Relationships
    user: User = Relationship(back_populates="budgets")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Analytics(SQLModel, table=True):
    """Analytics snapshot for performance optimization."""
    __tablename__ = "analytics"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Monthly aggregates
    year: int
    month: int
    total_income: float = Field(default=0.0)
    total_expenses: float = Field(default=0.0)
    net_balance: float = Field(default=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
