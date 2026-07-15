from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.features.chat.models import Conversation, Message


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_conversation(self, title: str) -> Conversation:
        conversation = Conversation(title=title)
        self._db.add(conversation)
        self._db.commit()
        self._db.refresh(conversation)
        return conversation

    def list_conversations(self) -> list[Conversation]:
        statement = select(Conversation).order_by(Conversation.updated_at.desc())
        return list(self._db.scalars(statement))

    def get_conversation(self, conversation_id: int) -> Conversation | None:
        statement = (
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        return self._db.scalar(statement)

    def add_message(self, conversation: Conversation, role: str, content: str) -> Message:
        message = Message(conversation=conversation, role=role, content=content)
        self._db.add(message)
        self._db.commit()
        self._db.refresh(message)
        return message
