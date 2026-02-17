"""
Settings and configuration for the FinanceFlow application.
Centralized configuration management.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App Config
    APP_NAME: str = "FinanceFlow"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database
    DATABASE_URL: str = "sqlite:///./data/finance_flow.db"
    DATABASE_ECHO: bool = DEBUG

    # Currency & Regional Settings
    CURRENCY: str = "EUR"
    DATE_FORMAT: str = "%d/%m/%Y"
    
    # Bank API Configuration (ready for real integration)
    BANK_API_PROVIDER: str = "mock"  # Options: 'mock', 'plaid', 'gocardless'
    BANK_API_KEY: Optional[str] = os.getenv("BANK_API_KEY", None)
    BANK_API_SECRET: Optional[str] = os.getenv("BANK_API_SECRET", None)

    # UI Configuration
    THEME: str = "dark"  # Options: 'light', 'dark'
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 800
    
    # Budget Defaults
    DEFAULT_MONTHLY_BUDGET: float = 3000.0
    CURRENCY_SYMBOL: str = "€"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    HASH_ALGORITHM: str = "sha256"

    # Directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOG_DIR: Path = BASE_DIR / "logs"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **data):
        super().__init__(**data)
        # Create necessary directories
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
