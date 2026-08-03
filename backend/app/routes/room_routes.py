from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import VideoRequest
from app.crud import set_video
from app.database import get_db
from app.schemas import JoinRoom, RoomResponse
from app.crud import (
    create_room,
    get_room_by_code,
    add_participant,
    get_participant
)

router = APIRouter(
    prefix="",
    tags=["Rooms"]
)


@router.post(
    "/create-room",
    response_model=RoomResponse
)
def create_new_room(
    db: Session = Depends(get_db)
):

    return create_room(db)


@router.post("/join-room")
def join_room(
    room: JoinRoom,
    db: Session = Depends(get_db)
):

    existing_room = get_room_by_code(
        db,
        room.room_code
    )

    if existing_room is None:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    participant = add_participant(
        db=db,
        username=room.username,
        room=existing_room
    )

    return {
        "room_code": existing_room.room_code,
        "participant_id": participant.id,
        "username": participant.username,
        "role": participant.role
    }


@router.post("/make-host/{room_code}/{username}")
def make_host(
    room_code: str,
    username: str,
    db: Session = Depends(get_db)
):

    room = get_room_by_code(
        db,
        room_code
    )

    if room is None:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    participant = get_participant(
        db,
        username,
        room.id
    )

    if participant is None:

        raise HTTPException(
            status_code=404,
            detail="Participant not found"
        )

    participant.role = "host"

    db.commit()

    db.refresh(participant)

    return {
        "message": f"{username} is now host"
    }


@router.get(
    "/room-state/{room_code}",
    response_model=RoomResponse
)
def room_state(
    room_code: str,
    db: Session = Depends(get_db)
):

    room = get_room_by_code(
        db,
        room_code
    )

    if room is None:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return room
@router.post("/set-video")
def update_video(data: VideoRequest, db: Session = Depends(get_db)):
    room = set_video(db, data.room_code, data.video_url)

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return room