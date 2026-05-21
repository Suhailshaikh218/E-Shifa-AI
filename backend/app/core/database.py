"""
Database connection and session management
"""
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Database instance
database = Database(settings.DATABASE_URL)

# SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata
metadata = MetaData()

# Base class for models
Base = declarative_base()


async def connect_db():
    """Connect to database"""
    await database.connect()
    print("✅ Database connected successfully")


async def disconnect_db():
    """Disconnect from database"""
    await database.disconnect()
    print("❌ Database disconnected")


async def get_db():
    """Dependency to get database session"""
    try:
        yield database
    finally:
        pass
