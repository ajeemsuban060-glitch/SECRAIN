from fastapi import APIRouter

from app.features.chat.api import router as chat_router
from app.features.memory.api import router as memory_router

api_router = APIRouter()

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

api_router.include_router(
    memory_router,
    prefix="/memory",
    tags=["Memory"],
)