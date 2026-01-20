from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Follow, CreatorVerification
from app.schemas import (
    UserOut,
    UserUpdate,
    CreatorVerificationCreate,
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# ===============================
# CONFIG: CATEGORIE SENSIBILI
# ===============================
SENSITIVE_CATEGORIES = {
    "medicina",
    "salute",
    "psicologia",
    "giurisprudenza",
    "diritto",
    "finanza",
    "investimenti",
    "nutrizione",
    "ingegneria",
    "fisioterapia",
}


# ===============================
# UTILITY
# ===============================
def build_user_response(user: User, db: Session) -> dict:
    followers_count = (
        db.query(Follow)
        .filter(Follow.following_id == user.id)
        .count()
    )

    following_count = (
        db.query(Follow)
        .filter(Follow.follower_id == user.id)
        .count()
    )

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "display_name": user.display_name,
        "bio_description": user.bio_description,
        "profile_image_url": user.profile_image_url,
        "role": user.role,
        "is_creator": user.is_creator,
        "is_creator_verified": user.is_creator_verified,
        "creator_verification": user.creator_verification,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "followers_count": followers_count,
        "following_count": following_count,
    }


# ===============================
# PROFILO PRIVATO
# GET /users/me
# ===============================
@router.get("/me", response_model=UserOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return build_user_response(current_user, db)


# ===============================
# UPDATE PROFILO
# PATCH /users/me
# ===============================
@router.patch("/me", response_model=UserOut)
def update_my_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.username and payload.username != current_user.username:
        exists = (
            db.query(User)
            .filter(User.username == payload.username)
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return build_user_response(current_user, db)


# ===============================
# BECOME CREATOR
# POST /users/become-creator
# ===============================
@router.post(
    "/become-creator",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
def become_creator(
    payload: CreatorVerificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.is_creator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a creator",
        )

    category_normalized = payload.category.lower().strip()

    # upgrade base
    current_user.is_creator = True
    current_user.role = "creator"

    # check if professional category
    if category_normalized in SENSITIVE_CATEGORIES:
        verification = CreatorVerification(
            user_id=current_user.id,
            category=category_normalized,
            degree_title=payload.degree_title,
            professional_register=payload.professional_register,
            identity_document_path="",
            degree_document_path="",
            status="pending",
        )
        db.add(verification)
        current_user.is_creator_verified = False
    else:
        # standard creator
        current_user.is_creator_verified = True

    db.commit()
    db.refresh(current_user)

    return build_user_response(current_user, db)


# ===============================
# PROFILO PUBBLICO
# GET /users/{username}
# ===============================
@router.get("/{username}", response_model=UserOut)
def get_user_profile(
    username: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return build_user_response(user, db)


# ===============================
# USER STATS
# GET /users/{username}/stats
# ===============================
@router.get(
    "/{username}/stats",
    status_code=status.HTTP_200_OK,
)
def get_user_stats(
    username: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    followers_count = (
        db.query(Follow)
        .filter(Follow.following_id == user.id)
        .count()
    )

    following_count = (
        db.query(Follow)
        .filter(Follow.follower_id == user.id)
        .count()
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "followers_count": followers_count,
        "following_count": following_count,
    }
