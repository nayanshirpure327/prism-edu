from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.domains.auth.schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, ForgotPasswordRequest, ResetPasswordRequest, EmailVerifyRequest
from app.domains.auth.service import AuthService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db = Depends(get_db)):
    return AuthService(db).register_user(data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db = Depends(get_db)):
    return AuthService(db).login_user(data)

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    return {"message": "Logged out"}

@router.post("/refresh")
async def refresh(data: RefreshRequest):
    return {"access_token": "new", "refresh_token": "new"}

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.post("/verify-email")
async def verify_email(data: EmailVerifyRequest):
    return {"message": "Email verified"}

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    return {"message": "Email sent"}

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    return {"message": "Password reset"}
