import CreateRoom from "../components/CreateRoom";
import JoinRoom from "../components/JoinRoom";

function Home() {
  return (
    <div className="home">

      <div className="home-container">

        <h1>
          🎬 YouTube Watch Party
        </h1>

        <p className="subtitle">
          Watch videos together with friends in real-time
        </p>


        <div className="cards">

          <div className="card">
            <h2>Create Room</h2>
            <p>
              Create a room and become the host.
            </p>

            <CreateRoom />
          </div>



          <div className="divider">
            OR
          </div>



          <div className="card">
            <h2>Join Room</h2>
            <p>
              Enter room code and watch together.
            </p>

            <JoinRoom />
          </div>

        </div>

      </div>

    </div>
  );
}

export default Home;