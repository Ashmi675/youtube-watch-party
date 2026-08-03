import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function JoinRoom() {

  const [roomCode, setRoomCode] = useState("");
  const [username, setUsername] = useState("");

  const navigate = useNavigate();


  const handleJoinRoom = async () => {

    if (!roomCode.trim() || !username.trim()) {
      alert("Enter room code and username");
      return;
    }


    try {

      await api.post("/join-room", {

        room_code: roomCode,

        username: username

      });


      navigate(`/room/${roomCode}`, {

        state: {
          username,
        },

      });


    } catch (error) {

      console.error(error);

      alert("Room not found");

    }

  };


  return (

    <div className="room-form">


      <input

        placeholder="Room Code"

        value={roomCode}

        onChange={(e) =>
          setRoomCode(e.target.value.toUpperCase())
        }

      />


      <input

        placeholder="Username"

        value={username}

        onChange={(e) =>
          setUsername(e.target.value)
        }

      />


      <button onClick={handleJoinRoom}>

        Join Room

      </button>


    </div>

  );

}


export default JoinRoom;