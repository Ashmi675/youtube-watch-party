from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routes.room_routes import router as room_router
from app.websocket import websocket_endpoint

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Watch Party",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://youtube-watch-party-vert.vercel.app",   # Your Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Watch Party Backend Running 🚀"
    }

# REST APIs
app.include_router(room_router)

# WebSocket Endpoint
app.websocket("/ws/{room_code}/{username}")(websocket_endpoint)