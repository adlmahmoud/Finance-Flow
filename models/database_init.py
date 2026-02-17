"""Database initialization and engine configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from config.settings import settings
from models.database import User, BankAccount, Transaction, Budget, Analytics


class DatabaseManager:
    """Database connection and session management."""
    
    _engine = None
    _session_maker = None

    @classmethod
    def init_db(cls):
        """Initialize database engine and create tables."""
        if cls._engine is None:
            cls._engine = create_engine(
                settings.DATABASE_URL,
                echo=settings.DATABASE_ECHO,
                connect_args={"check_same_thread": False},  # For SQLite
            )
            
            # Create all tables
            SQLModel.metadata.create_all(cls._engine)
            
            # Create session factory
            cls._session_maker = sessionmaker(
                bind=cls._engine,
                class_=Session,
                expire_on_commit=False,
            )
        
        return cls._engine

    @classmethod
    def get_session(cls) -> Session:
        """Get a new database session."""
        if cls._session_maker is None:
            cls.init_db()
        return cls._session_maker()

    @classmethod
    def close_session(cls, session: Session):
        """Close a database session."""
        if session:
            session.close()

    @classmethod
    def get_engine(cls):
        """Get the database engine."""
        if cls._engine is None:
            cls.init_db()
        return cls._engine
