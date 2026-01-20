from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import User, CreatorVerification
from app.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin/creators",
    tags=["admin-creators"],
)


# ===============================
# SCHEMAS (LOCAL)
# ===============================
class RejectCreatorPayload(BaseModel):
    admin_note: str = Field(..., min_length=5, max_length=500)


# ===============================
# GET CREATOR REQUESTS
# GET /admin/creators?status_filter=pending
# ===============================
@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_creator_requests(
    status_filter: str = Query(
        "pending",
        description="pending | verified | rejected",
    ),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return (
        db.query(CreatorVerification)
        .filter(CreatorVerification.status == status_filter)
        .order_by(CreatorVerification.created_at.asc())
        .all()
    )


# ===============================
# APPROVE CREATOR
# POST /admin/creators/{verification_id}/approve
# ===============================
@router.post(
    "/{verification_id}/approve",
    status_code=status.HTTP_200_OK,
)
def approve_creator(
    verification_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    verification = (
        db.query(CreatorVerification)
        .filter(CreatorVerification.id == verification_id)
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification request not found",
        )

    if verification.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification already processed",
        )

    verification.status = "verified"
    verification.reviewed_at = datetime.now(timezone.utc)
    verification.admin_note = None

    user = (
        db.query(User)
        .filter(User.id == verification.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated user not found",
        )

    # ✅ ALLINEAMENTO STATO UTENTE
    user.is_creator = True
    user.is_creator_verified = True

    db.commit()
    db.refresh(verification)
    db.refresh(user)

    return verification


# ===============================
# REJECT CREATOR
# POST /admin/creators/{verification_id}/reject
# ===============================
@router.post(
    "/{verification_id}/reject",
    status_code=status.HTTP_200_OK,
)
def reject_creator(
    verification_id: int,
    payload: RejectCreatorPayload,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    verification = (
        db.query(CreatorVerification)
        .filter(CreatorVerification.id == verification_id)
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification request not found",
        )

    if verification.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification already processed",
        )

    verification.status = "rejected"
    verification.admin_note = payload.admin_note
    verification.reviewed_at = datetime.now(timezone.utc)

    user = (
        db.query(User)
        .filter(User.id == verification.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated user not found",
        )

    # ✅ ALLINEAMENTO STATO UTENTE (FIX LOGICO)
    user.is_creator = False
    user.is_creator_verified = False

    db.commit()
    db.refresh(verification)
    db.refresh(user)

    return verification
