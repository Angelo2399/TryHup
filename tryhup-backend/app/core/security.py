from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from jose import jwt, JWTError

# ===============================
# CONFIG JWT
# ===============================
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 ore


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY non impostata nell'ambiente")


# ===============================
# CREATE ACCESS TOKEN
# ===============================
def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


# ===============================
# DECODE ACCESS TOKEN
# ===============================
def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        subject = payload.get("sub")
        if not subject:
            raise JWTError("Token senza subject")

        return subject

    except JWTError as e:
        raise ValueError("Token non valido o scaduto") from e
