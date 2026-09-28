from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    app_name: str = "PRISM-EDU"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    base_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://prism_user:prism_dev_password@localhost:5432/prism_edu"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False

    # Auth / JWT
    auth_secret: str = "CHANGE_ME_TO_A_STRONG_RANDOM_SECRET_MIN_32_CHARS"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # OpenAI
    openai_api_key: str = ""
    openai_model_primary: str = "gpt-4o"
    openai_model_secondary: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_max_tokens: int = 4096
    openai_request_timeout_seconds: int = 30
    ai_response_cache_ttl_seconds: int = 3600

    # S3 / MinIO
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key_id: str = "minioadmin"
    s3_secret_access_key: str = "minioadmin_dev_password"
    s3_bucket_name: str = "prism-edu-storage"
    s3_region: str = "us-east-1"

    # Email
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "noreply@prismedu.app"
    smtp_from_name: str = "PRISM-EDU"
    smtp_use_tls: bool = False

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Rate Limiting
    rate_limit_per_minute_anonymous: int = 30
    rate_limit_per_minute_authenticated: int = 120
    rate_limit_per_minute_ai_endpoints: int = 20

    # Celery
    celery_broker_url: str = "redis://localhost:6379/3"
    celery_result_backend: str = "redis://localhost:6379/4"

    # Feature Flags
    feature_ai_explanations: bool = True
    feature_rag_enabled: bool = False
    feature_parent_access: bool = True
    feature_counselor_workflows: bool = True
    feature_report_generation: bool = True

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",")]
        return v


settings = Settings()
