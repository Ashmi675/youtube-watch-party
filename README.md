# YouTube Watch Party

A real-time YouTube Watch Party application that enables multiple users to watch YouTube videos together in synchronized playback. The application supports role-based controls, participant management, and seamless real-time communication using WebSockets.

## Live Demo

**Frontend:** https://youtube-watch-party-vert.vercel.app

**Backend:** https://youtube-watch-party-tsln.onrender.com

---

##  Features

- Create and join watch party rooms
-  Real-time synchronized video playback
-  Play, Pause and Seek synchronization
-  Live participant list
-  Host and Moderator roles
-  Role-based playback controls
-  Remove participants from the room
-  Late join synchronization
-  Real-time communication using WebSockets
-  Responsive and modern user interface

---

##  Tech Stack

### Frontend

- React.js
- Vite
- JavaScript
- CSS3
- Axios
- React Router DOM
- React YouTube

### Backend

- FastAPI
- Python
- WebSockets
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

### Deployment

- Vercel (Frontend)
- Render (Backend)

---

##  Project Structure

```
youtube-watch-party/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── websocket.py
│   │   ├── message_handler.py
│   │   ├── room_manager.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── watchparty.db
│
└── README.md
```

---

##  Installation

### Clone Repository

```bash
git clone https://github.com/<your-username>/youtube-watch-party.git

cd youtube-watch-party
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn app.main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

## Application Workflow

1. Create a watch party room.
2. Share the room code with participants.
3. Participants join the room.
4. Host loads a YouTube video.
5. Play, Pause and Seek actions are synchronized across all connected users.
6. Host can promote moderators or remove participants.
7. New participants automatically sync with the current playback state.

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/create-room` | Create a new room |
| POST | `/join-room` | Join existing room |
| POST | `/set-video` | Set room video |
| GET | `/room-state/{room_code}` | Get current room state |

---

## WebSocket Endpoint

```
/ws/{room_code}/{username}
```

Used for:

- Play Sync
- Pause Sync
- Seek Sync
- Role Updates
- Participant Updates
- Video Changes
- Remove Participant

---

## Author

**Ashmi Singh**

GitHub: https://github.com/Ashmi675

LinkedIn: https://www.linkedin.com/in/ashmi-singh-881686298

---

## License

This project is created for learning and portfolio purposes.
