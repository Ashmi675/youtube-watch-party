from sqlalchemy.orm import Session

from app.models import Room, Participant
from app.utils import generate_room_code


def create_room(db: Session):

    room = Room(

        room_code=generate_room_code()

    )

    db.add(room)

    db.commit()

    db.refresh(room)

    return room


def get_room_by_code(
    db: Session,
    room_code: str
):

    return (

        db.query(Room)

        .filter(Room.room_code == room_code)

        .first()

    )


def add_participant(
    db: Session,
    username: str,
    room: Room,
    role="viewer"
):

    participant = Participant(

        username=username,

        role=role,

        room_id=room.id

    )

    db.add(participant)

    db.commit()

    db.refresh(participant)

    return participant


def get_participant(
    db: Session,
    username: str,
    room_id: int
):

    return (

        db.query(Participant)

        .filter(

            Participant.username == username,

            Participant.room_id == room_id

        )

        .first()

    )


def update_room_state(
    db: Session,
    room: Room,
    video_id: str,
    current_time: int,
    playback_state: str
):

    room.current_video = video_id

    room.current_time = current_time

    room.playback_state = playback_state

    db.commit()

    db.refresh(room)

    return room
def set_video(db: Session, room_code: str, video_url: str):
    room = db.query(Room).filter(Room.room_code == room_code).first()

    if not room:
        return None

    room.current_video = video_url
    db.commit()
    db.refresh(room)

    return room