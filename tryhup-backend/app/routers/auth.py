from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import random
import smtplib
import os
import logging
from email.message import EmailMessage
from pydantic import BaseModel

from app.database import get_db
from app.models import User, LoginCode
from app.schemas import AuthRequestCode, AuthVerifyCode, AuthTokenOut
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

DEV_MODE = os.getenv("DEV_MODE") == "true"


# ===============================
# EMAIL SENDER
# ===============================
def send_login_code(email: str, code: str):
    msg = EmailMessage()
    msg["Subject"] = "TryHup – Codice di accesso"
    msg["From"] = os.getenv("EMAIL_FROM", "TryHup <noreply@tryhup.com>")
    msg["To"] = email
    msg.set_content(f"Il tuo codice di accesso TryHup è: {code}")

    with smtplib.SMTP(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT")),
    ) as server:
        server.starttls()
        server.login(
            os.getenv("SMTP_USER"),
            os.getenv("SMTP_PASSWORD"),
        )
        server.send_message(msg)


# ===============================
# REQUEST LOGIN CODE (PROD)
# ===============================
@router.post("/request-code", status_code=status.HTTP_200_OK)
def request_code(
    payload: AuthRequestCode,
    db: Session = Depends(get_db),
):
    db.query(LoginCode).filter(
        LoginCode.email == payload.email,
        LoginCode.used.is_(False),
    ).update({"used": True})

    db.commit()

    code = str(random.randint(100000, 999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    login_code = LoginCode(
        email=payload.email,
        code=code,
        expires_at=expires_at,
        used=False,
    )

    db.add(login_code)
    db.commit()

    send_login_code(payload.email, code)

    return {"message": "Login code sent"}


# ===============================
# VERIFY LOGIN CODE (PROD)
# ===============================
@router.post(
    "/verify-code",
    response_model=AuthTokenOut,
    status_code=status.HTTP_200_OK,
)
def verify_code(
    payload: AuthVerifyCode,
    db: Session = Depends(get_db),
):
    login_code = (
        db.query(LoginCode)
        .filter(
            LoginCode.email == payload.email,
            LoginCode.used.is_(False),
            LoginCode.expires_at > datetime.now(timezone.utc),
        )
        .order_by(LoginCode.created_at.desc())
        .first()
    )

    if not login_code or login_code.code != payload.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired code",
        )

    login_code.used = True

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        user = User(
            email=payload.email,
            role="user",
            is_active=True,
        )
        db.add(user)

    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email)

    return AuthTokenOut(
        access_token=token,
        profile_completed=user.username is not None,
    )


# ===============================
# DEV LOGIN (FAKE USERS)
# ===============================
class DevLoginPayload(BaseModel):
    email: str
    role: str = "user"


@router.post(
    "/dev-login",
    response_model=AuthTokenOut,
    status_code=status.HTTP_200_OK,
)
def dev_login(
    payload: DevLoginPayload,
    db: Session = Depends(get_db),
):
    if not DEV_MODE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="DEV_MODE disabled",
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        user = User(
            email=payload.email,
            role=payload.role,
            is_active=True,
            is_creator=False,
            is_creator_verified=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(subject=user.email)

    return AuthTokenOut(
        access_token=token,
        profile_completed=user.username is not None,
    )
