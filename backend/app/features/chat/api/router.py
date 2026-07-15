from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.ollama import OllamaUnavailableError
from app.database.session import get_db
from app.features.chat.schemas import ChatReply, ConversationCreate, ConversationRead, ConversationSummary, MessageCreate
from app.features.chat.service import ChatService, ConversationNotFoundError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def chat_status():
    return {"module": "chat", "status": "ready"}


@router.get("/conversations", response_model=list[ConversationSummary])
def list_conversations(db: Session = Depends(get_db)):
    return ChatService(db).list_conversations()


@router.post("/conversations", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    return ChatService(db).create_conversation(payload.title)


@router.get("/conversations/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    try:
        return ChatService(db).get_conversation(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")


@router.post("/conversations/{conversation_id}/messages", response_model=ChatReply)
async def send_message(conversation_id: int, payload: MessageCreate, db: Session = Depends(get_db)):
    try:
        result = await ChatService(db).send_message(conversation_id, payload.content)
        return {
            "message": result.message,
            "referenced_notes": [{"id": note.id, "title": note.title} for note in result.referenced_notes],
        }
    except ConversationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    except OllamaUnavailableError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))
