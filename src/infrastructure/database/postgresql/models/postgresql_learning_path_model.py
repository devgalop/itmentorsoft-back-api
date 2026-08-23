from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from datetime import datetime

from src.infrastructure.database.postgresql.models.postgresql_resource_content import (
    ResourceContentEntity,
)
from src.infrastructure.database.postgresql.models.postgresql_user_model import (
    UserEntity,
)
from src.infrastructure.database.postgresql.shared.postgresql_database_session import (
    Base,
)


class LearningPathEntity(Base):
    __tablename__ = "learning_paths"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    topic: Mapped[str] = mapped_column(String, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.now,
        server_onupdate=func.now(),
    )

    user: Mapped[UserEntity] = relationship("UserEntity")
    contents: Mapped[list["LearningPathContentEntity"]] = relationship(
        "LearningPathContentEntity", back_populates="learning_path"
    )


class LearningPathContentEntity(Base):
    __tablename__ = "learning_path_contents"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    learning_path_id: Mapped[str] = mapped_column(
        String, ForeignKey("learning_paths.id"), index=True
    )
    content_id: Mapped[str] = mapped_column(
        String, ForeignKey("contents.id"), index=True
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.now(),
        server_onupdate=func.now(),
    )

    learning_path: Mapped[LearningPathEntity] = relationship(
        "LearningPathEntity", back_populates="contents"
    )
    content: Mapped[ResourceContentEntity] = relationship("ResourceContentEntity")
