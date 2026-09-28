from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import AuthenticationError, ConflictError


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, data):
        result = self.db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise ConflictError("User already exists")

        role_val = getattr(data, "role", "STUDENT")
        if isinstance(role_val, str):
            role_enum = UserRole[role_val.upper()]
        else:
            role_enum = role_val

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            role=role_enum
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        user_dict = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role)
        }
        return {
            "user": user_dict,
            "access_token": create_access_token(user_dict),
            "refresh_token": create_refresh_token(user_dict),
            "token_type": "bearer"
        }

    def login_user(self, data):
        result = self.db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        user_dict = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role)
        }
        return {
            "user": user_dict,
            "access_token": create_access_token(user_dict),
            "refresh_token": create_refresh_token(user_dict),
            "token_type": "bearer"
        }
