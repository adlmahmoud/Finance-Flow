"""
Bank API Integration Service.
Handles connection to external bank APIs (Plaid, GoCardless) with mock fallback.
Ready for production API integration.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
import random

from loguru import logger
from config.settings import settings
from models.database import Transaction, TransactionType, TransactionCategory


class BankProvider(str, Enum):
    """Supported bank providers."""
    MOCK = "mock"
    PLAID = "plaid"
    GOCARDLESS = "gocardless"


class BaseBankService(ABC):
    """Abstract base class for bank service providers."""

    @abstractmethod
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with bank API."""
        pass

    @abstractmethod
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get list of accounts."""
        pass

    @abstractmethod
    def get_transactions(self, account_id: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get transactions for an account."""
        pass

    @abstractmethod
    def get_balance(self, account_id: str) -> float:
        """Get account balance."""
        pass


class MockBankService(BaseBankService):
    """
    Mock Bank Service - Simulates bank API for development.
    Generates realistic mock data.
    """

    def __init__(self):
        """Initialize mock service."""
        self.accounts = self._generate_mock_accounts()
        logger.info("MockBankService initialized")

    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Mock authentication always succeeds."""
        logger.info("Mock authentication successful")
        return True

    def _generate_mock_accounts(self) -> List[Dict[str, Any]]:
        """Generate mock bank accounts."""
        return [
            {
                "id": "mock_account_001",
                "name": "Compte Courant",
                "bank": "Banque XYZ",
                "balance": 2500.50,
                "currency": "EUR",
            },
            {
                "id": "mock_account_002",
                "name": "Compte Épargne",
                "bank": "Banque XYZ",
                "balance": 5000.00,
                "currency": "EUR",
            },
        ]

    def get_accounts(self) -> List[Dict[str, Any]]:
        """Return mock accounts."""
        return self.accounts

    def get_balance(self, account_id: str) -> float:
        """Get balance for mock account."""
        for account in self.accounts:
            if account["id"] == account_id:
                return account["balance"]
        return 0.0

    def get_transactions(self, account_id: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Generate realistic mock transactions.
        
        Args:
            account_id: Account identifier
            days_back: Number of days to generate transactions for
            
        Returns:
            List of mock transactions
        """
        transactions = []
        
        # Mock merchants and categories
        mock_data = {
            TransactionCategory.FOOD: [
                {"merchants": ["Carrefour", "E.Leclerc", "Intermarche", "Restaurant du Coin"],
                 "amounts": [25, 50, 100, 35, 45]},
            ],
            TransactionCategory.TRANSPORT: [
                {"merchants": ["RATP", "SNCF", "Shell", "Essence Station"],
                 "amounts": [15, 90, 60, 55]},
            ],
            TransactionCategory.UTILITIES: [
                {"merchants": ["EDF", "Orange", "Aqua Plus"],
                 "amounts": [120, 25, 40]},
            ],
            TransactionCategory.ENTERTAINMENT: [
                {"merchants": ["Netflix", "Spotify", "Cinéma", "Jeux Vidéo"],
                 "amounts": [12, 10, 15, 60]},
            ],
            TransactionCategory.SHOPPING: [
                {"merchants": ["Zara", "H&M", "Amazon", "Décathlon"],
                 "amounts": [45, 35, 50, 25]},
            ],
            TransactionCategory.HEALTHCARE: [
                {"merchants": ["Pharmacie", "Docteur", "Dentiste"],
                 "amounts": [25, 50, 150]},
            ],
        }

        # Generate transactions
        for i in range(random.randint(15, 30)):  # 15-30 transactions
            days_ago = random.randint(0, days_back)
            date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Random expense category
            category = random.choice(list(mock_data.keys()))
            data = mock_data[category][0]
            merchant = random.choice(data["merchants"])
            amount = random.choice(data["amounts"])
            
            transactions.append({
                "id": f"mock_txn_{date.timestamp()}_{i}",
                "account_id": account_id,
                "description": merchant,
                "merchant": merchant,
                "amount": float(amount),
                "category": category,
                "transaction_type": TransactionType.EXPENSE,
                "date": date.isoformat(),
                "external_id": f"ext_{i}",
            })

        # Add random income (monthly salary)
        if random.random() > 0.7:
            salary_date = datetime.utcnow().replace(day=1, hour=9, minute=0, second=0)
            transactions.append({
                "id": f"mock_salary_{salary_date.timestamp()}",
                "account_id": account_id,
                "description": "Salaire Mensuel",
                "merchant": "Employeur",
                "amount": 2500.0,
                "category": TransactionCategory.SALARY,
                "transaction_type": TransactionType.INCOME,
                "date": salary_date.isoformat(),
                "external_id": "salary_001",
            })

        return sorted(transactions, key=lambda x: x["date"], reverse=True)


class PlaidBankService(BaseBankService):
    """
    Plaid Bank Service - Production integration with Plaid API.
    To be implemented with actual Plaid SDK.
    """

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Plaid service.
        
        Args:
            access_token: Plaid access token
        """
        self.access_token = access_token or settings.BANK_API_KEY
        logger.info("PlaidBankService initialized (mock mode)")

    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """
        Authenticate with Plaid API.
        TODO: Implement actual Plaid client authentication.
        """
        logger.warning("Plaid authentication not yet implemented")
        return False

    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get accounts from Plaid API."""
        logger.warning("Plaid get_accounts not yet implemented")
        return []

    def get_transactions(self, account_id: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get transactions from Plaid API."""
        logger.warning("Plaid get_transactions not yet implemented")
        return []

    def get_balance(self, account_id: str) -> float:
        """Get account balance from Plaid API."""
        logger.warning("Plaid get_balance not yet implemented")
        return 0.0


class GoCardlessService(BaseBankService):
    """
    GoCardless Bank Service - Production integration with GoCardless API.
    To be implemented with actual GoCardless SDK.
    """

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize GoCardless service.
        
        Args:
            access_token: GoCardless access token
        """
        self.access_token = access_token or settings.BANK_API_KEY
        logger.info("GoCardlessService initialized (mock mode)")

    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with GoCardless API."""
        logger.warning("GoCardless authentication not yet implemented")
        return False

    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get accounts from GoCardless API."""
        logger.warning("GoCardless get_accounts not yet implemented")
        return []

    def get_transactions(self, account_id: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get transactions from GoCardless API."""
        logger.warning("GoCardless get_transactions not yet implemented")
        return []

    def get_balance(self, account_id: str) -> float:
        """Get account balance from GoCardless API."""
        logger.warning("GoCardless get_balance not yet implemented")
        return 0.0


class BankServiceFactory:
    """Factory for creating appropriate bank service instance."""

    _services = {
        BankProvider.MOCK: MockBankService,
        BankProvider.PLAID: PlaidBankService,
        BankProvider.GOCARDLESS: GoCardlessService,
    }

    @classmethod
    def create(cls, provider: str = None) -> BaseBankService:
        """
        Create bank service instance.
        
        Args:
            provider: Provider name (defaults to settings.BANK_API_PROVIDER)
            
        Returns:
            Bank service instance
        """
        provider = provider or settings.BANK_API_PROVIDER
        
        if provider not in cls._services:
            logger.warning(f"Unknown provider {provider}, falling back to MOCK")
            provider = BankProvider.MOCK

        service_class = cls._services[provider]
        logger.info(f"Creating {service_class.__name__}")
        return service_class()
