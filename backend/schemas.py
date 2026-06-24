"""Purpose: Pydantic request/response schemas for API validation."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "user",
                "password": "securepassword123"
            }
        }


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response after login/register."""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class UserInfo(BaseModel):
    """User information."""
    id: int
    email: str
    username: str
    created_at: datetime
    api_calls_today: int


class APIResponse(BaseModel):
    """Generic API response."""
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
