import os
from fastapi import Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.core.security import decode_access_token


# ===============================
# CONFIG DEV AUTH
# ===============================
DEV_MODE = os.getenv("DEV_MODE") == "true"


# ===============================
# GET CURRENT USER
# ===============================
def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    x_dev_email: str | None = Header(default=None, alias="X-DEV-EMAIL"),
    x_dev_role: str | None = Header(default=None, alias="X-DEV-ROLE"),
) -> User:
    """
    PRIORITÀ:
    1️⃣ DEV MODE + X-DEV-EMAIL (+ opzionale X-DEV-ROLE)
    2️⃣ JWT Bearer
    """

    # ===============================
    # DEV MODE (FAKE USERS)
    # ===============================
    if DEV_MODE and x_dev_email:
        role = x_dev_role if x_dev_role in {"user", "admin"} else "user"

        user = (
            db.query(User)
            .filter(User.email == x_dev_email)
            .first()
        )

        if not user:
            user = User(
                email=x_dev_email,
                role=role,
                is_active=True,
                is_creator=False,
                is_creator_verified=False,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # 🔁 aggiorna ruolo se cambiato
            if user.role != role:
                user.role = role
                db.commit()
                db.refresh(user)

        return user

    # ===============================
    # JWT FLOW (PROD)
    # ===============================
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
        )

    token = parts[1]

    try:
        email = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


# ===============================
# GET CURRENT ADMIN
# ===============================
def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user
