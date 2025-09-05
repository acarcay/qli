from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import timedelta
from app.core.security import create_access_token
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


# NOTE: Placeholder logic; replace with real user lookup
def _verify(email: str, password: str) -> bool:
    return email.endswith("@example.com") and password == "password"


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    if not _verify(payload.email, payload.password):
        raise HTTPException(status_code=400, detail="invalid credentials")
    token = create_access_token(payload.email, settings.JWT_SECRET, timedelta(hours=12))
    return TokenResponse(access_token=token)


