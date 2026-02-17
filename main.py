"""
FinanceFlow - Modern Expense Management Application
Entry point for the application.

Usage:
    python main.py
"""

import logging
from pathlib import Path

from loguru import logger
from config.settings import settings
from models.database_init import DatabaseManager
from ui.main_app import main
import flet as ft


# Configure logging
log_file = settings.LOG_DIR / "financeflow.log"
logger.remove()
logger.add(
    log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
)
logger.add(
    lambda msg: print(msg, end=""),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="INFO",
)

logger.info("=" * 60)
logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
logger.info("=" * 60)


def init_application():
    """Initialize the application."""
    try:
        # Initialize database
        logger.info("Initializing database...")
        DatabaseManager.init_db()
        logger.info("✓ Database initialized")

        # Initialize logging
        logger.info(f"✓ Logging configured: {log_file}")

        # Log configuration
        logger.info(f"APP_NAME: {settings.APP_NAME}")
        logger.info(f"DATABASE: {settings.DATABASE_URL}")
        logger.info(f"THEME: {settings.THEME}")
        logger.info(f"BANK_PROVIDER: {settings.BANK_API_PROVIDER}")
        
    except Exception as e:
        logger.error(f"Application initialization failed: {e}")
        raise


if __name__ == "__main__":
    # Initialize application
    init_application()

    # Start Flet application
    logger.info("Starting UI...")
    ft.app(main)

    logger.info("Application closed")
