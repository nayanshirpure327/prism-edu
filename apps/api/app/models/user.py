from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class UserRole(enum.Enum):
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    COUNSELOR = "COUNSELOR"
    ADMIN = "ADMIN"

class DataStatus(enum.Enum):
    VERIFIED = "VERIFIED"
    NEEDS_VERIFICATION = "NEEDS_VERIFICATION"
    EXPIRED = "EXPIRED"
    HISTORICAL = "HISTORICAL"
    ESTIMATED = "ESTIMATED"
    USER_PROVIDED = "USER_PROVIDED"

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"
    user_id = Column(ForeignKey("users.id"))
    token_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
