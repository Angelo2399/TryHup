from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Text,
    Index,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


# ===============================
# USERS
# ===============================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)

    username = Column(String, unique=True, index=True, nullable=True)
    display_name = Column(String, nullable=True)
    bio_description = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)

    # roles: user | admin | creator
    role = Column(String, default="user", nullable=False)

    is_creator = Column(Boolean, default=False, nullable=False)
    is_creator_verified = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # relationships
    contents = relationship(
        "Content",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )

    creator_verification = relationship(
        "CreatorVerification",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


# ===============================
# CREATOR VERIFICATION
# ===============================
class CreatorVerification(Base):
    __tablename__ = "creator_verifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    category = Column(String, nullable=False)

    # public info
    degree_title = Column(String, nullable=False)
    professional_register = Column(String, nullable=True)

    # document paths (private storage)
    identity_document_path = Column(String, nullable=False)
    degree_document_path = Column(String, nullable=False)
    register_document_path = Column(String, nullable=True)

    # pending | verified | rejected
    status = Column(String, default="pending", nullable=False)

    admin_note = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    reviewed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User", back_populates="creator_verification")

    __table_args__ = (
        Index("idx_creator_verifications_status", "status"),
    )


# ===============================
# FOLLOW SYSTEM
# ===============================
class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)

    follower_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    following_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    follower = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following",
    )

    following = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers",
    )

    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_follow",
        ),
    )


# ===============================
# CONTENT
# ===============================
class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)

    media_type = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    creator_description = Column(Text, nullable=False)
    category = Column(String, nullable=True)

    approved = Column(Boolean, default=False, nullable=False)

    rating_avg = Column(Integer, default=0, nullable=False)
    rating_count = Column(Integer, default=0, nullable=False)
    growth_index = Column(Integer, default=1, nullable=False)
    growth_percentage = Column(Integer, default=25, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owner = relationship("User", back_populates="contents")

    comments = relationship(
        "Comment",
        back_populates="content",
        cascade="all, delete-orphan",
    )

    likes = relationship(
        "Like",
        back_populates="content",
        cascade="all, delete-orphan",
    )


# ===============================
# LIKES
# ===============================
class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    content_id = Column(
        Integer,
        ForeignKey("contents.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="likes")
    content = relationship("Content", back_populates="likes")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "content_id",
            name="unique_like",
        ),
    )


# ===============================
# COMMENTS
# ===============================
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    content_id = Column(
        Integer,
        ForeignKey("contents.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    text = Column(Text, nullable=False)

    parent_id = Column(
        Integer,
        ForeignKey("comments.id"),
        nullable=True,
    )

    is_approved = Column(Boolean, default=False, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)

    moderation_score = Column(Integer, default=0, nullable=False)
    moderation_note = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    author = relationship("User", back_populates="comments")
    content = relationship("Content", back_populates="comments")


# ===============================
# LOGIN CODE
# ===============================
class LoginCode(Base):
    __tablename__ = "login_codes"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
