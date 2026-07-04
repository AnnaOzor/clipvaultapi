from datetime import datetime
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from database import Base
from schemas import ClipStatus


class Clips(Base):
    __tablename__ = "clips"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    upload_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    status: Mapped[ClipStatus] = mapped_column(
        Enum(ClipStatus),
        nullable=False
    )