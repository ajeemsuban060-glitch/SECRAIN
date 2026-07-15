from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.base import Base
from app.database.database import engine
from app.features.chat.api.router import router as chat_router
from app.features.notes.api.router import router as notes_router

# Register SQLAlchemy models
from app.features.chat.models import Conversation, Message
from app.features.memory.models import Memory
from app.features.notes.models import Note

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(notes_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Welcome to SECRAIN"
    }
