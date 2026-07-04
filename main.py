from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
import models
from models import Clips
from database import engine, SessionLocal
from datetime import datetime

from schemas import ClipStatusUpdate, ClipRequest, ClipStatus, ClipResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/clips",  response_model=list[ClipResponse], status_code=status.HTTP_200_OK)
async def read_all_clips(
    db: db_dependency,
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of clips to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of clips to skip"
    ),
    clip_status: Optional[ClipStatus] = Query(
        default=None,
        alias="status",
        description="Filter clips by status"
    )
):
    query = db.query(Clips)

    if clip_status is not None:
        query = query.filter(
            Clips.status == clip_status.value
        )

    return query.offset(offset).limit(limit).all()

@app.get("/clips/{clip_id}", status_code=status.HTTP_200_OK)
async def read_clip(
    db: db_dependency,
    clip_id: int = Path(
        ...,
        gt=0,
        description="Unique clip ID"
    )
):
    clip = db.query(Clips).filter(Clips.id == clip_id).first()

    if clip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with ID {clip_id} not found."
        )

    return clip


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {
        "status": "healthy",
        "service": "Clip Vault API",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.post("/clips", status_code=status.HTTP_201_CREATED)
async def create_clip(
    clip_request: ClipRequest,
    db: db_dependency
):
    existing_clip = (
        db.query(Clips)
        .filter(Clips.filename == clip_request.filename)
        .first()
    )

    if existing_clip:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A clip with this filename already exists."
        )

    new_clip = Clips(
        title=clip_request.title,
        filename=clip_request.filename,
        upload_time=datetime.now(),
        status=clip_request.status.value
    )

    db.add(new_clip)
    db.commit()
    db.refresh(new_clip)

    return {
        "message": "Clip created successfully.",
        "clip": new_clip
    }

@app.patch(
    "/clips/{clip_id}",
    status_code=status.HTTP_200_OK,
    summary="Update clip status",
    description="Updates the status of an existing clip."
)
async def update_clip_status(
    update: ClipStatusUpdate,
    db: db_dependency,
    clip_id: int = Path(
        ...,
        gt=0,
        description="Unique clip ID"
    )
):
    clip = db.query(Clips).filter(Clips.id == clip_id).first()

    if clip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with ID {clip_id} not found."
        )

    clip.status = update.status.value

    db.commit()
    db.refresh(clip)

    return {
        "message": f"Clip status updated to '{clip.status}'.",
        "clip": clip
    }

@app.delete("/clips/{clip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clip(
    db: db_dependency,
    clip_id: int = Path(
        ...,
        gt=0,
        description="Unique clip ID"
    )
):
    clip = db.query(Clips).filter(Clips.id == clip_id).first()

    if clip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with ID {clip_id} not found."
        )

    db.delete(clip)
    db.commit()