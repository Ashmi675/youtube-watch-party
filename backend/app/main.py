from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes.room_routes import router as room_router
from app.websocket import websocket_endpoint
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YouTube Watch Party",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():

    return {
        "message": "Watch Party Backend Running 🚀"
    }


app.include_router(room_router)
app.websocket("/ws/{room_code}/{username}")(websocket_endpoint)
