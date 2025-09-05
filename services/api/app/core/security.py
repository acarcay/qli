from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt

ALGORITHM = "HS256"


def create_access_token(subject: str, secret: str, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    to_encode: dict[str, Any] = {"sub": subject, "iat": int(now.timestamp())}
    if expires_delta:
        to_encode.update({"exp": int((now + expires_delta).timestamp())})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def verify_token(token: str, secret: str) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=[ALGORITHM])


