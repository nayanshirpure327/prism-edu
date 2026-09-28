import os
import textwrap
from pathlib import Path

base_dir = Path(r"C:\Users\GHOST\.gemini\antigravity\scratch\prism-edu\apps\api")

dirs = [
    "app/core", "app/models", "app/domains/auth", "app/domains/profile",
    "app/domains/careers", "app/domains/institutions", "app/domains/scholarships",
    "app/domains/finance", "app/domains/pathways", "app/domains/scenarios",
    "app/domains/decision_matrix", "app/domains/assessments", "app/domains/reports",
    "app/domains/notifications", "app/domains/admin", "alembic/versions",
    "database/seeds/mock", "scripts"
]
for d in dirs:
    (base_dir / d).mkdir(parents=True, exist_ok=True)

def write_file(path, content):
    with open(base_dir / path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip())

# 1. requirements.txt
write_file("requirements.txt", """
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0
pydantic>=2.7.0
pydantic-settings>=2.3.0
python-jose[cryptography]>=3.3.0
bcrypt>=4.1.0
python-multipart>=0.0.9
aioredis>=2.0.0
httpx>=0.27.0
celery>=5.4.0
openai>=1.30.0
numpy>=1.26.0
pgvector>=0.2.5
python-slugify>=8.0.0
pillow>=10.3.0
reportlab>=4.2.0
email-validator>=2.1.0
aiosmtplib>=3.0.0
boto3>=1.34.0
slowapi>=0.7.0
""")

# 2. requirements-dev.txt
write_file("requirements-dev.txt", """
-r requirements.txt
pytest>=8.2.0
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0
httpx>=0.27.0
factory-boy>=3.3.0
faker>=25.0.0
ruff>=0.4.0
mypy>=1.10.0
bandit>=1.7.0
""")

# 3. app/__init__.py
write_file("app/__init__.py", "")
write_file("app/core/__init__.py", "")
write_file("app/models/__init__.py", """
from app.models.base import Base
from app.models.user import User, RefreshToken
from app.models.profile import StudentProfile, AcademicRecord, WorkPreference, ParentStudentLink, CounselorStudentAssignment
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAnswer, AssessmentResult
from app.models.career import Industry, Skill, Career, CareerSkill, SavedItem
from app.models.education import Country, EducationSystem, Institution, Program, ProgramRequirement, Scholarship, LoanProduct
from app.models.pathway import Pathway, PathwayStep, Scenario, ScenarioChange, DecisionMatrixResult, Report, Notification, AuditLog
""")
write_file("app/domains/__init__.py", "")

# 4. app/main.py
write_file("app/main.py", """
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.exceptions import PrismException
from app.core.database import check_db_connection
from app.core.redis import check_redis_connection
from app.domains.auth.router import router as auth_router
from app.domains.profile.router import router as profile_router
import time

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="PRISM-EDU API Backend",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(PrismException)
async def prism_exception_handler(request: Request, exc: PrismException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.error_code, "message": exc.message, "details": exc.details}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request parameters", "details": exc.errors()}}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}}
    )

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["profile"])

@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "healthy", "timestamp": time.time(), "version": settings.app_version}

@app.get("/ready", tags=["system"])
async def ready_check():
    db_ok = await check_db_connection()
    redis_ok = await check_redis_connection()
    status_code = 200 if db_ok and redis_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "ready" if status_code == 200 else "unavailable", "db": db_ok, "redis": redis_ok}
    )
""")

# 6. app/core/config.py
write_file("app/core/config.py", """
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "PRISM-EDU"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    base_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"
    
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/prismedu"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_echo: bool = False
    
    jwt_algorithm: str = "RS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7
    auth_secret: str = "supersecretkey_replace_in_prod"
    
    redis_url: str = "redis://localhost:6379/0"
    
    openai_api_key: str = ""
    openai_model_primary: str = "gpt-4-turbo"
    openai_model_secondary: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    
    s3_endpoint_url: str = ""
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""
    s3_bucket_name: str = ""
    
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    
    allowed_origins: List[str] = ["*"]
    
    rate_limit_per_minute_anonymous: int = 60
    rate_limit_per_minute_authenticated: int = 120
    
    feature_ai_explanations: bool = True
    feature_rag_enabled: bool = True
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
""")

# 7. app/core/database.py
write_file("app/core/database.py", """
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    echo=settings.db_echo,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def check_db_connection():
    try:
        async with engine.connect() as conn:
            return True
    except Exception:
        return False
""")

# 8. app/core/security.py
write_file("app/core/security.py", """
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.auth_secret, algorithm="HS256")

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.auth_secret, algorithm="HS256")
""")

# 9. app/core/exceptions.py
write_file("app/core/exceptions.py", """
from fastapi import status

class PrismException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = "BAD_REQUEST", details: dict = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

class AuthenticationError(PrismException):
    def __init__(self, message="Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "AUTH_ERROR")

class AuthorizationError(PrismException):
    def __init__(self, message="Not authorized"):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "FORBIDDEN")

class NotFoundError(PrismException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND, "NOT_FOUND")
""")

# 10. app/core/redis.py
write_file("app/core/redis.py", """
import aioredis
from app.core.config import settings

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)

async def get_redis():
    return redis_client

async def cache_get(key: str):
    return await redis_client.get(key)

async def cache_set(key: str, value: str, expire: int = 3600):
    await redis_client.set(key, value, ex=expire)

async def cache_delete(key: str):
    await redis_client.delete(key)

async def check_redis_connection():
    try:
        await redis_client.ping()
        return True
    except Exception:
        return False
""")

# 12. app/models/base.py
write_file("app/models/base.py", """
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    created_at = Column(DateTime, server_default=text('now()'))
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
""")

# Generate remaining models stubs and minimal routers
write_file("app/models/user.py", """
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
""")

write_file("app/models/profile.py", "from .base import BaseModel\nclass StudentProfile(BaseModel): __tablename__ = 'student_profiles'\nclass AcademicRecord(BaseModel): __tablename__ = 'academic_records'\nclass WorkPreference(BaseModel): __tablename__ = 'work_preferences'\nclass ParentStudentLink(BaseModel): __tablename__ = 'parent_student_links'\nclass CounselorStudentAssignment(BaseModel): __tablename__ = 'counselor_student_assignments'\n")
write_file("app/models/assessment.py", "from .base import BaseModel\nclass Assessment(BaseModel): __tablename__ = 'assessments'\nclass AssessmentQuestion(BaseModel): __tablename__ = 'assessment_questions'\nclass AssessmentAttempt(BaseModel): __tablename__ = 'assessment_attempts'\nclass AssessmentAnswer(BaseModel): __tablename__ = 'assessment_answers'\nclass AssessmentResult(BaseModel): __tablename__ = 'assessment_results'\n")
write_file("app/models/career.py", "from .base import BaseModel\nclass Industry(BaseModel): __tablename__ = 'industries'\nclass Skill(BaseModel): __tablename__ = 'skills'\nclass Career(BaseModel): __tablename__ = 'careers'\nclass CareerSkill(BaseModel): __tablename__ = 'career_skills'\nclass SavedItem(BaseModel): __tablename__ = 'saved_items'\n")
write_file("app/models/education.py", "from .base import BaseModel\nclass Country(BaseModel): __tablename__ = 'countries'\nclass EducationSystem(BaseModel): __tablename__ = 'education_systems'\nclass Institution(BaseModel): __tablename__ = 'institutions'\nclass Program(BaseModel): __tablename__ = 'programs'\nclass ProgramRequirement(BaseModel): __tablename__ = 'program_requirements'\nclass Scholarship(BaseModel): __tablename__ = 'scholarships'\nclass LoanProduct(BaseModel): __tablename__ = 'loan_products'\n")
write_file("app/models/pathway.py", "from .base import BaseModel\nclass Pathway(BaseModel): __tablename__ = 'pathways'\nclass PathwayStep(BaseModel): __tablename__ = 'pathway_steps'\nclass Scenario(BaseModel): __tablename__ = 'scenarios'\nclass ScenarioChange(BaseModel): __tablename__ = 'scenario_changes'\nclass DecisionMatrixResult(BaseModel): __tablename__ = 'decision_matrix_results'\nclass Report(BaseModel): __tablename__ = 'reports'\nclass Notification(BaseModel): __tablename__ = 'notifications'\nclass AuditLog(BaseModel): __tablename__ = 'audit_logs'\n")

# Routers
write_file("app/domains/auth/router.py", """
from fastapi import APIRouter
router = APIRouter()
@router.post("/register")
async def register(): return {"status": "ok"}
""")
write_file("app/domains/profile/router.py", """
from fastapi import APIRouter
router = APIRouter()
@router.get("/")
async def get_profile(): return {"status": "ok"}
""")

print("Successfully generated all essential PRISM-EDU backend scaffolding files.")
