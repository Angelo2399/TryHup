from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment, User
from app.schemas import CommentOut
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/admin/comments",
    tags=["admin-comments"],
)


# ===============================
# ADMIN GUARD
# ===============================
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only",
        )
    return current_user


# ===============================
# LIST COMMENTS
# GET /admin/comments?status=pending
# ===============================
@router.get(
    "",
    response_model=list[CommentOut],
)
def list_comments(
    status: str = Query("pending", enum=["pending", "approved", "flagged"]),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    query = db.query(Comment)

    if status == "pending":
        query = query.filter(Comment.is_approved.is_(False))
    elif status == "approved":
        query = query.filter(Comment.is_approved.is_(True))
    elif status == "flagged":
        query = query.filter(Comment.is_flagged.is_(True))

    return query.order_by(Comment.created_at.desc()).all()


# ===============================
# APPROVE COMMENT
# PATCH /admin/comments/{id}/approve
# ===============================
@router.patch(
    "/{comment_id}/approve",
    response_model=CommentOut,
)
def approve_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.is_approved = True
    comment.is_flagged = False

    db.commit()
    db.refresh(comment)

    return comment


# ===============================
# REJECT / FLAG COMMENT
# PATCH /admin/comments/{id}/reject
# ===============================
@router.patch(
    "/{comment_id}/reject",
    response_model=CommentOut,
)
def reject_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.is_approved = False
    comment.is_flagged = True

    db.commit()
    db.refresh(comment)

    return comment
