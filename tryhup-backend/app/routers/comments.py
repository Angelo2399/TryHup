from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment, Content, User
from app.schemas import CommentCreate, CommentOut
from app.dependencies import get_current_user
from app.services.moderation import moderate_comment


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


# ===============================
# CREATE COMMENT
# POST /comments/{content_id}
# ===============================
@router.post(
    "/{content_id}",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    content_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = (
        db.query(Content)
        .filter(
            Content.id == content_id,
            Content.approved.is_(True),
        )
        .first()
    )

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found or not approved",
        )

    moderation = moderate_comment(payload.text)

    comment = Comment(
        content_id=content_id,
        user_id=current_user.id,
        text=payload.text,
        is_approved=moderation["is_approved"],
        is_flagged=moderation["is_flagged"],
        moderation_score=moderation["score"],
        moderation_note=moderation["note"],
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# ===============================
# GET COMMENTS FOR CONTENT
# GET /comments/{content_id}
# ===============================
@router.get(
    "/{content_id}",
    response_model=list[CommentOut],
)
def get_comments_for_content(
    content_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Comment)
        .filter(
            Comment.content_id == content_id,
            Comment.is_approved.is_(True),
        )
        .order_by(Comment.created_at.asc())
        .all()
    )
