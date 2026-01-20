from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.database import get_db
from app.models import Content, Follow, User
from app.schemas import ContentCreate, ContentOut, RatingIn, FeedResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/contents",
    tags=["contents"],
)


# ===============================
# CREATE CONTENT
# POST /contents
# ===============================
@router.post(
    "/",
    response_model=ContentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_content(
    payload: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = Content(
        media_type=payload.media_type,
        media_url=payload.media_url,
        creator_description=payload.creator_description,
        category=payload.category,
        owner_id=current_user.id,
        approved=False,
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    return content


# ===============================
# RATE CONTENT
# POST /contents/{content_id}/rate
# ===============================
@router.post(
    "/{content_id}/rate",
    status_code=status.HTTP_200_OK,
)
def rate_content(
    content_id: int,
    payload: RatingIn,
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
            detail="Content not found",
        )

    total_score = content.rating_avg * content.rating_count
    content.rating_count += 1
    content.rating_avg = (total_score + payload.rating) / content.rating_count

    db.commit()

    return {"message": "Rating submitted successfully"}


# ===============================
# UNIFIED FEED (FOLLOWING → DISCOVER)
# GET /contents/feed
# ===============================
@router.get(
    "/feed",
    response_model=FeedResponse,
    status_code=status.HTTP_200_OK,
)
def unified_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    """
    Feed unico:
    1️⃣ Contenuti degli utenti seguiti
    2️⃣ Fallback automatico su Discover
    """

    following_subquery = (
        db.query(Follow.following_id)
        .filter(Follow.follower_id == current_user.id)
        .subquery()
    )

    # ---------------------------
    # 1️⃣ FOLLOWING FEED
    # ---------------------------
    following_query = (
        db.query(Content)
        .filter(
            Content.approved.is_(True),
            Content.owner_id.in_(following_subquery),
        )
        .order_by(desc(Content.created_at))
    )

    following_total = following_query.count()

    following_items = (
        following_query
        .limit(limit)
        .offset(offset)
        .all()
    )

    if following_items:
        return FeedResponse(
            items=following_items,
            limit=limit,
            offset=offset,
            total=following_total,
        )

    # ---------------------------
    # 2️⃣ DISCOVER FALLBACK
    # ---------------------------
    discover_query = (
        db.query(Content)
        .filter(
            Content.approved.is_(True),
            Content.owner_id.not_in(following_subquery),
        )
        .order_by(
            desc(Content.growth_index),
            desc(Content.rating_avg),
            func.random(),
        )
    )

    discover_total = discover_query.count()

    discover_items = (
        discover_query
        .limit(limit)
        .offset(offset)
        .all()
    )

    return FeedResponse(
        items=discover_items,
        limit=limit,
        offset=offset,
        total=discover_total,
    )
