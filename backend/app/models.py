from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    room_code = Column(
        String,
        unique=True,
        nullable=False
    )

    current_video = Column(
        String,
        nullable=True
    )

    current_time = Column(
        Integer,
        default=0
    )

    playback_state = Column(
        String,
        default="paused"
    )

    participants = relationship(
        "Participant",
        back_populates="room",
        cascade="all, delete"
    )


class Participant(Base):

    __tablename__ = "participants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="viewer"
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id")
    )

    room = relationship(
        "Room",
        back_populates="participants"
    )