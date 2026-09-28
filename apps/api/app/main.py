from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import uuid
import time

from app.core.config import settings
from app.core.database import init_db, check_db_connection
from app.core.exceptions import PrismException

# ── Logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}',
)
logger = logging.getLogger("prism_edu")

# ── Lifespan ─────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("PRISM-EDU API starting up...")
    init_db()
    logger.info("Database connection initialized.")
    yield
    logger.info("PRISM-EDU API shutting down.")

# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="PRISM-EDU API",
    description="Career Path Simulator — AI-powered Education & Career Decision-Support Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request ID Middleware ─────────────────────────────────────
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# ── Exception Handlers ────────────────────────────────────────
@app.exception_handler(PrismException)
async def prism_exception_handler(request: Request, exc: PrismException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": exc.errors(),
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again.",
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )

# ── Health Endpoints ──────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "version": "0.1.0", "service": "prism-edu-api"}

@app.get("/ready", tags=["System"])
async def ready():
    db_ok = check_db_connection()
    if not db_ok:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "unavailable"},
        )
    return {"status": "ready", "database": "connected"}

# ── Routers ───────────────────────────────────────────────────
from app.domains.auth.router import router as auth_router
from app.domains.profile.router import router as profile_router
from app.domains.careers.router import router as careers_router
from app.domains.assessments.router import router as assessments_router
from app.domains.institutions.router import router as institutions_router
from app.domains.scholarships.router import router as scholarships_router
from app.domains.finance.router import router as finance_router
from app.domains.pathways.router import router as pathways_router
from app.domains.scenarios.router import router as scenarios_router
from app.domains.decision_matrix.router import router as decision_matrix_router
from app.domains.reports.router import router as reports_router
from app.domains.notifications.router import router as notifications_router
from app.domains.admin.router import router as admin_router

# Versioned routes (/api/v1)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(assessments_router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(careers_router, prefix="/api/v1/careers", tags=["Careers"])
app.include_router(institutions_router, prefix="/api/v1/institutions", tags=["Institutions"])
app.include_router(scholarships_router, prefix="/api/v1/scholarships", tags=["Scholarships"])
app.include_router(finance_router, prefix="/api/v1/loans", tags=["Finance & Loans"])
app.include_router(pathways_router, prefix="/api/v1/pathways", tags=["Pathways"])
app.include_router(scenarios_router, prefix="/api/v1/scenarios", tags=["Scenarios"])
app.include_router(decision_matrix_router, prefix="/api/v1/decision-matrix", tags=["Decision Matrix"])
app.include_router(reports_router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])

# Legacy / direct web routes (/api)
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"], include_in_schema=False)
app.include_router(profile_router, prefix="/api/profile", tags=["Profile"], include_in_schema=False)
app.include_router(assessments_router, prefix="/api/assessments", tags=["Assessments"], include_in_schema=False)
app.include_router(careers_router, prefix="/api/careers", tags=["Careers"], include_in_schema=False)
app.include_router(institutions_router, prefix="/api/institutions", tags=["Institutions"], include_in_schema=False)
app.include_router(scholarships_router, prefix="/api/scholarships", tags=["Scholarships"], include_in_schema=False)
app.include_router(finance_router, prefix="/api/loans", tags=["Finance & Loans"], include_in_schema=False)
app.include_router(pathways_router, prefix="/api/pathways", tags=["Pathways"], include_in_schema=False)
app.include_router(scenarios_router, prefix="/api/scenarios", tags=["Scenarios"], include_in_schema=False)
app.include_router(decision_matrix_router, prefix="/api/matrix", tags=["Decision Matrix"], include_in_schema=False)
app.include_router(decision_matrix_router, prefix="/api/decision-matrix", tags=["Decision Matrix"], include_in_schema=False)
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"], include_in_schema=False)
app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"], include_in_schema=False)
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"], include_in_schema=False)
