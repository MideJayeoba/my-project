"""Purpose: Authentication utilities for JWT and password handling."""

import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))
RATE_LIMIT_CALLS_PER_DAY = int(os.getenv("RATE_LIMIT_CALLS_PER_DAY", "1000"))


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """Create JWT token with expiration."""
    if expires_delta is None:
        expires_delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    payload = {"user_id": user_id, "exp": expire}
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire


def verify_token(token: str) -> Optional[int]:
    """Verify JWT token and return user_id if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except jwt.InvalidTokenError:
        return None
