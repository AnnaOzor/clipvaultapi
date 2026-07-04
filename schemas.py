from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClipStatus(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"


class ClipRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the video clip"
    )

    filename: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Video filename including extension"
    )

    status: ClipStatus = Field(
        default=ClipStatus.uploaded,
        description="Current processing status of the clip"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My Holiday",
                "filename": "holiday.mp4",
                "status": "uploaded"
            }
        }
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank.")

        return value

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        allowed_extensions = (
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
            ".webm",
        )

        if not value.lower().endswith(allowed_extensions):
            raise ValueError(
                "Filename must end with .mp4, .mov, .avi, .mkv, or .webm."
            )

        return value


class ClipStatusUpdate(BaseModel):
    status: ClipStatus = Field(
        ...,
        description="New status for the clip"
    )

class ClipResponse(BaseModel):
    id: int
    title: str
    filename: str
    upload_time: datetime
    status: ClipStatus

    model_config = ConfigDict(
        from_attributes=True
    )