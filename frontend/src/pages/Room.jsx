import { useParams, useLocation } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import YouTube from "react-youtube";
import "./Room.css";

function Room() {

  const { roomCode } = useParams();
  const location = useLocation();

  const username = location.state?.username;

  const [role, setRole] = useState("");
  const [participants, setParticipants] = useState([]);
  const [videoUrl, setVideoUrl] = useState("");
  const [videoId, setVideoId] = useState("");

  const socketRef = useRef(null);
  const playerRef = useRef(null);

  const syncing = useRef(false);
  const seekTimeout = useRef(null);
  const [removed, setRemoved] = useState(false);

  const canControl =
    role === "host" ||
    role === "moderator";

  const extractVideoId = (url) => {

    const regex =
      /(?:youtube\.com\/.*v=|youtu\.be\/)([^&\n?#]+)/;

    const match = url.match(regex);

    return match ? match[1] : null;

  };

  const sendMessage = (data) => {

    if (
      socketRef.current &&
      socketRef.current.readyState === WebSocket.OPEN
    ) {

      socketRef.current.send(
        JSON.stringify(data)
      );

    }

  };

  const loadVideo = async () => {

    const id =
      extractVideoId(videoUrl);

    if (!id) {

      alert("Invalid YouTube URL");
      return;

    }

    try {

      await axios.post(
        "http://127.0.0.1:8000/set-video",
        {
          room_code: roomCode,
          video_url: id
        }
      );

      setVideoId(id);

      sendMessage({

        action: "CHANGE_VIDEO",

        videoId: id

      });

    }
    catch (err) {

      console.log(err);

    }

  };

  const makeModerator = (user) => {

    sendMessage({

      action: "ROLE",

      target: user,

      role: "moderator"

    });

  };

  const removeUser = (user) => {

    sendMessage({

      action: "REMOVE",

      target: user

    });

  };

  useEffect(() => {

    if (!username)
      return;

    const socket =
      new WebSocket(
        `ws://youtube-watch-party-tsln.onrender.com/ws/${roomCode}/${username}`
      );

    socketRef.current = socket;

    socket.onopen = () => {

      console.log("Connected");

    };

    socket.onmessage = (event) => {

      const data =
        JSON.parse(event.data);

      switch (data.type) {

        case "JOIN":
          setRole(data.role);
          setParticipants(data.participants);
          // late join sync
          if(data.video){
            if(data.video.videoId){
              setVideoId(data.video.videoId);
              setVideoUrl(
                `https://youtube.com/watch?v=${data.video.videoId}`
              );
            }
            setTimeout(() => {
              if(playerRef.current){
                playerRef.current.seekTo(
                  data.video.currentTime,
                  true
                );
                if(data.video.playState === "playing"){
                  playerRef.current.playVideo();
                }
                else{
                  playerRef.current.pauseVideo();
                }
              }
            },1000);
          }
        break;

        case "PARTICIPANTS_UPDATE":

          setParticipants(
            data.participants
          );

          break;

        case "ROLE":

          if (
            data.username === username
          ) {

            setRole(data.role);

          }

          setParticipants(prev =>
            prev.map(user =>
              user.username === data.username
                ? {
                    ...user,
                    role: data.role
                  }
                : user
            )
          );

          break;

        case "REMOVE":

          setParticipants(prev =>
            prev.filter(
              user =>
                user.username !==
                data.username
            )
          );

          break;
          case "KICKED":
            if (playerRef.current) {
              playerRef.current.stopVideo();
            }
            if (socketRef.current) {
              socketRef.current.close();
            }
            setRemoved(true);
          break;

          case "CHANGE_VIDEO":
            syncing.current = true;
            setVideoId(data.videoId);
            setVideoUrl(
              `https://youtube.com/watch?v=${data.videoId}`
            );
            setTimeout(() => {
              syncing.current = false;
            }, 200);
            break;
          case "PLAY":

          if (!playerRef.current)
            break;

          syncing.current = true;

          // latency compensate
          playerRef.current.seekTo(
            data.currentTime,
            true
          );

          playerRef.current.playVideo();

          setTimeout(() => {

            syncing.current = false;

          }, 300);

          break;



        case "PAUSE":

          if (!playerRef.current)
            break;

          syncing.current = true;

          playerRef.current.seekTo(
            data.currentTime,
            true
          );

          playerRef.current.pauseVideo();

          setTimeout(() => {

            syncing.current = false;

          }, 300);

          break;



        case "SEEK":

          if (!playerRef.current)
            break;

          const localTime =
          playerRef.current.getCurrentTime();

          const diff =
          Math.abs(localTime - data.currentTime);
          if (diff < 0.5) {
            break;
          }

          syncing.current = true;

          playerRef.current.seekTo(
            data.currentTime,
            true
          );

          setTimeout(() => {

            syncing.current = false;

          }, 250);

          break;
          default:
            break;
          }
          };
          socket.onerror = (err) => {
            console.log(err);
          };
          return () => {
            socket.close();
            if (seekTimeout.current) {
              clearTimeout(seekTimeout.current);
            }
          };
          }, [roomCode, username]);
          useEffect(() => {

            const getState = async () => {
        
              try {
        
                const res = await axios.get(
                  `http://127.0.0.1:8000/room-state/${roomCode}`
                );
        
                if (res.data.current_video) {
        
                  setVideoId(res.data.current_video);
        
                  setVideoUrl(
                    `https://youtube.com/watch?v=${res.data.current_video}`
                  );
        
                }
        
              }
              catch (err) {
        
                console.log(err);
        
              }
        
            };
        
            getState();
        
          }, [roomCode]);
          if (removed) {

            return (
          
              <div className="removed-page">
          
                <div className="removed-card">
          
                  <h1>
                     You were removed
                  </h1>
          
                  <p>
                    The host removed you from this watch party.
                  </p>
          
          
                  <button
                    onClick={() => window.location.href="/"}
                  >
                    Go Home
                  </button>
          
          
                </div>
          
              </div>
          
            );
          
          }
          
        
        
        
          return (

            <div className="room-page">
            
            
              <div className="room-header">
            
                <h1>
                  🎬 YouTube Watch Party
                </h1>
            
                <div className="room-info">
            
                  <span>
                    Room: <b>{roomCode}</b>
                  </span>
            
                  <span>
                    User: <b>{username}</b>
                  </span>
            
                  <span>
                    Role: <b>{role}</b>
                  </span>
            
                </div>
            
              </div>
            
            
            
              <div className="room-content">
            
            
                <div className="video-area">
            
            
                  {canControl &&
            
                  <div className="video-control">
            
                    <input
                      placeholder="Paste YouTube URL"
                      value={videoUrl}
                      onChange={(e)=>setVideoUrl(e.target.value)}
                    />
            
                    <button onClick={loadVideo}>
                      Load
                    </button>
            
                  </div>
            
                  }
            
            
            
                  <div className="video-card">
            
                  {
                    videoId ? (
            
                    <YouTube
                      key={videoId}
                      videoId={videoId}
            
                      onReady={(event)=>{
            
                        playerRef.current = event.target;
            
                        playerRef.current.__lastSeekTime = 0;
            
                        if(videoId){
                          playerRef.current.cueVideoById(videoId);
                        }
            
                      }}
            
            
                      onPlay={()=>{
                        if(
                          syncing.current ||
                          !canControl ||
                          !playerRef.current
                        )
                        return;
            
            
                        sendMessage({
            
                          action:"PLAY",
            
                          currentTime:
                          playerRef.current.getCurrentTime()
            
                        });
            
                      }}
            
            
                      onPause={()=>{
            
                        if(
                          syncing.current ||
                          !canControl ||
                          !playerRef.current
                        )
                        return;
            
            
                        sendMessage({
            
                          action:"PAUSE",
            
                          currentTime:
                          playerRef.current.getCurrentTime()
            
                        });
            
                      }}
            
            
                      onStateChange={(event)=>{
            
                        if(
                          syncing.current ||
                          !canControl ||
                          !playerRef.current
                        )
                        return;
            
            
                        if(
                          event.data !== window.YT.PlayerState.PLAYING
                        )
                        return;
            
            
                        if(seekTimeout.current)
                          clearTimeout(seekTimeout.current);
            
            
            
                        seekTimeout.current=setTimeout(()=>{
            
            
                          const currentTime =
                          playerRef.current.getCurrentTime();
            
            
            
                          const previousTime =
                          playerRef.current.__lastSeekTime || 0;
            
            
            
                          if(
                            Math.abs(currentTime-previousTime)>3
                          ){
            
                            sendMessage({
            
                              action:"SEEK",
            
                              currentTime
            
                            });
            
                          }
            
            
            
                          playerRef.current.__lastSeekTime =
                          currentTime;
            
            
            
                        },500);
            
            
            
                      }}
            
            
                      opts={{
            
                        width:"100%",
                        height:"450",
            
                        playerVars:{
                          autoplay:0,
                          playsinline:1,
                          rel:0,
                          modestbranding:1,
                          origin:window.location.origin
                        }
            
                      }}
            
                    />
                  ) : (

                    <div className="empty-video">

                      <h2>🎬 No video loaded</h2>

                      <p>
                        Host can add a YouTube video to start watching
                      </p>

                    </div>

                  )
            
            
                  }
            
                  </div>
            
            
                </div>
            
            
            
            
            
                <div className="participants-card">
            
            
                  <h2>
                    👥 Participants
                  </h2>
            
            
                  {
                    participants.map(user=>(
            
                      <div
                        className="participant"
                        key={user.username}
                      >
            
                        <span>
                          {user.username}
                          <small>
                            {user.role}
                          </small>
                        </span>
            
            
                        {
                          role==="host" &&
                          user.username!==username &&
            
                          <div>
            
                            <button
                              onClick={()=>makeModerator(user.username)}
                            >
                              Promote
                            </button>
            
            
                            <button
                              onClick={()=>removeUser(user.username)}
                            >
                              Remove
                            </button>
            
                          </div>
            
                        }
            
            
                      </div>
            
                    ))
                  }
            
            
                </div>
            
            
              </div>
            
            
            </div>
            
            );
        
        }
        
        export default Room;
        
        
        
        