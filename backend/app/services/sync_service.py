from sqlalchemy.orm import Session

from app.crud import (
    get_room_by_code,
    update_room_state,
)


class SyncService:

    def change_video(
        self,
        db: Session,
        room_code: str,
        video_id: str
    ):
        room = get_room_by_code(db, room_code)

        if not room:
            return None

        return update_room_state(
            db=db,
            room=room,
            video_id=video_id,
            current_time=0,
            playback_state="paused"
        )

    def play(
        self,
        db: Session,
        room_code: str,
        current_time: float
    ):
        room = get_room_by_code(db, room_code)

        if not room:
            return None

        return update_room_state(
            db=db,
            room=room,
            video_id=room.current_video,
            current_time=current_time,
            playback_state="playing"
        )

    def pause(
        self,
        db: Session,
        room_code: str,
        current_time: float
    ):
        room = get_room_by_code(db, room_code)

        if not room:
            return None

        return update_room_state(
            db=db,
            room=room,
            video_id=room.current_video,
            current_time=current_time,
            playback_state="paused"
        )

    def seek(
        self,
        db: Session,
        room_code: str,
        current_time: float
    ):
        room = get_room_by_code(db, room_code)

        if not room:
            return None

        return update_room_state(
            db=db,
            room=room,
            video_id=room.current_video,
            current_time=current_time,
            playback_state=room.playback_state
        )

    def get_state(
        self,
        db: Session,
        room_code: str
    ):
        return get_room_by_code(db, room_code)


sync_service = SyncService()