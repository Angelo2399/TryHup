from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Like, Content, User
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
)


# ===============================
# LIKE CONTENT
# POST /likes/{content_id}
# ===============================
@router.post(
    "/{content_id}",
    status_code=status.HTTP_201_CREATED,
)
def like_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    existing = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.content_id == content_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Content already liked",
        )

    like = Like(
        user_id=current_user.id,
        content_id=content_id,
    )

    content.like_count += 1

    db.add(like)
    db.commit()

    return {"message": "Content liked"}


# ===============================
# UNLIKE CONTENT
# DELETE /likes/{content_id}
# ===============================
@router.delete(
    "/{content_id}",
    status_code=status.HTTP_200_OK,
)
def unlike_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.content_id == content_id,
        )
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=404,
            detail="Like not found",
        )

    content = db.query(Content).filter(Content.id == content_id).first()
    if content:
        content.like_count = max(content.like_count - 1, 0)

    db.delete(like)
    db.commit()

    return {"message": "Content unliked"}
