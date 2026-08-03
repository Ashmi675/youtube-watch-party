import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function CreateRoom() {

  const navigate = useNavigate();

  const [username, setUsername] = useState("");


  const handleCreateRoom = async () => {

    if (!username.trim()) {
      alert("Enter username");
      return;
    }


    try {

      const response = await api.post("/create-room");


      navigate(`/room/${response.data.room_code}`, {

        state: {
          username,
        },

      });


    } catch (error) {

      console.log(error);

      alert("Failed to create room");

    }

  };


  return (

    <div className="room-form">

      <input

        type="text"

        placeholder="Enter username"

        value={username}

        onChange={(e) => setUsername(e.target.value)}

      />


      <button onClick={handleCreateRoom}>

        Create Room

      </button>


    </div>

  );

}


export default CreateRoom;