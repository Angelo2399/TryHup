from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Content, User
from app.schemas import ContentOut
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


# ===============================
# ADMIN CHECK
# ===============================
def require_admin(user: User):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )


# ===============================
# CONTENT MODERATION
# ===============================

@router.get(
    "/contents",
    response_model=list[ContentOut],
    status_code=status.HTTP_200_OK,
)
def get_all_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    approved: bool | None = Query(
        None,
        description="Filter by approval status",
    ),
):
    require_admin(current_user)

    query = db.query(Content)

    if approved is not None:
        query = query.filter(Content.approved == approved)

    return query.order_by(Content.created_at.desc()).all()


@router.post(
    "/contents/{content_id}/approve",
    status_code=status.HTTP_200_OK,
)
def approve_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    content = (
        db.query(Content)
        .filter(Content.id == content_id)
        .first()
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found",
        )

    content.approved = True
    db.commit()

    return {"message": "Content approved successfully"}
