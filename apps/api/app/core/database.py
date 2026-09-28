from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
import logging
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

# Standard SQLite for local Windows dev without blocked C-extensions
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../prism_edu.db"))
SYNC_DB_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    SYNC_DB_URL,
    connect_args={"check_same_thread": False},
    echo=settings.db_echo
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Verify DB connectivity and initialize schema."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Database connection verified at {SYNC_DB_URL}.")

        # Auto-create all tables
        import app.models  # register all models
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema synchronized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")


def check_db_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
