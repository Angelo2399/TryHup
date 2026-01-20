from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Follow
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/follows",
    tags=["follows"],
)

# ===============================
# FOLLOW USER
# POST /follows/{user_id}
# ===============================
@router.post(
    "/{user_id}",
    status_code=status.HTTP_201_CREATED,
)
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself",
        )

    target_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == user_id,
        )
        .first()
    )
    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user",
        )

    follow = Follow(
        follower_id=current_user.id,
        following_id=user_id,
    )

    db.add(follow)
    db.commit()

    return {"message": "User followed successfully"}


# ===============================
# UNFOLLOW USER
# DELETE /follows/{user_id}
# ===============================
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == user_id,
        )
        .first()
    )

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user",
        )

    db.delete(follow)
    db.commit()

    return {"message": "User unfollowed successfully"}


# ===============================
# LIST FOLLOWERS
# GET /follows/{user_id}/followers
# ===============================
@router.get(
    "/{user_id}/followers",
    status_code=status.HTTP_200_OK,
)
def list_followers(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    followers = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.following_id == user_id)
        .all()
    )

    return followers


# ===============================
# LIST FOLLOWING
# GET /follows/{user_id}/following
# ===============================
@router.get(
    "/{user_id}/following",
    status_code=status.HTTP_200_OK,
)
def list_following(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    following = (
        db.query(User)
        .join(Follow, Follow.following_id == User.id)
        .filter(Follow.follower_id == user_id)
        .all()
    )

    return following
