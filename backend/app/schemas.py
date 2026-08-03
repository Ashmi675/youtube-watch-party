from pydantic import BaseModel


class CreateRoom(BaseModel):
    pass


class JoinRoom(BaseModel):

    room_code: str

    username: str


class RoomResponse(BaseModel):

    id: int

    room_code: str

    current_video: str | None = None

    current_time: int

    playback_state: str

    class Config:

        from_attributes = True


class ParticipantResponse(BaseModel):

    id: int

    username: str

    role: str

    class Config:

        from_attributes = True
class VideoRequest(BaseModel):
    room_code: str
    video_url: str