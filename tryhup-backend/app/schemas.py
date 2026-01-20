from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# ===============================
# USERS
# ===============================

class CreatorVerificationPublic(BaseModel):
    category: str
    degree_title: str
    professional_register: Optional[str]
    status: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: str

    username: Optional[str]
    display_name: Optional[str]
    bio_description: Optional[str]
    profile_image_url: Optional[str]

    role: str
    is_creator: bool
    is_creator_verified: bool

    creator_verification: Optional[CreatorVerificationPublic]

    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9_]+$",
    )
    display_name: Optional[str] = Field(None, max_length=50)
    bio_description: Optional[str] = Field(None, max_length=160)
    profile_image_url: Optional[str]


# ===============================
# CREATOR VERIFICATION (INPUT)
# ===============================

class CreatorVerificationCreate(BaseModel):
    category: str
    degree_title: str
    professional_register: Optional[str] = None


class CreatorVerificationStatus(BaseModel):
    status: str
    admin_note: Optional[str] = None


# ===============================
# CONTENT
# ===============================

class ContentCreate(BaseModel):
    media_type: str = Field(..., pattern="^(video|image)$")
    media_url: str
    creator_description: str
    category: Optional[str] = None


class RatingIn(BaseModel):
    rating: int = Field(..., ge=1, le=5)


class ContentOut(BaseModel):
    id: int
    media_type: str
    media_url: str
    creator_description: str
    category: Optional[str]

    owner_id: Optional[int]

    approved: bool
    rating_avg: float
    rating_count: int
    growth_index: int
    growth_percentage: int

    created_at: datetime

    class Config:
        from_attributes = True


# ===============================
# FEED
# ===============================

class FeedResponse(BaseModel):
    items: List[ContentOut]
    limit: int
    offset: int
    total: int


# ===============================
# COMMENTS
# ===============================

class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    parent_id: Optional[int] = None


class CommentOut(BaseModel):
    id: int
    content_id: int
    user_id: int
    text: str

    parent_id: Optional[int]

    is_approved: bool
    is_flagged: bool
    moderation_score: int
    moderation_note: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True


# ===============================
# AUTH
# ===============================

class AuthRequestCode(BaseModel):
    email: str


class AuthVerifyCode(BaseModel):
    email: str
    code: str = Field(..., min_length=6, max_length=6)


class AuthTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    profile_completed: bool
