import re
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.notes.models import Note

_STOP_WORDS = {
    "a", "an", "and", "are", "about", "at", "be", "by", "can",
    "did", "do", "does", "for", "from", "have", "how", "i",
    "in", "is", "it", "me", "my", "of", "on", "or", "the",
    "to", "was", "what", "when", "where", "which", "who",
    "with", "you", "your"
}

NOTE_QUERY_TERMS = {
    "note",
    "notes",
    "saved",
    "save",
    "remember",
    "memory",
    "memories",
    "wrote",
    "written",
    "write",
    "summarize",
    "summary"
}

RECENT_QUERY_TERMS = {
    "today",
    "yesterday",
    "recent",
    "latest",
    "last"
}


@dataclass(frozen=True)
class RetrievedNote:
    id: int
    title: str
    summary: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    def as_context(self) -> str:
        tags = ", ".join(self.tags) if self.tags else "None"

        return (
            f"Title: {self.title}\n"
            f"Summary: {self.summary or 'No summary'}\n"
            f"Tags: {tags}\n"
            f"Created: {self.created_at}\n"
            f"Updated: {self.updated_at}\n\n"
            f"Content:\n{self.content}"
        )


class NoteRetriever:
    """
    Local SQLite note retriever.

    This implementation is intentionally isolated so it can later
    be replaced by a ChromaDB semantic retriever without changing
    ChatService.
    """

    def __init__(self, db: Session):
        self._db = db

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z0-9]+", text.lower())
            if len(token) > 1 and token not in _STOP_WORDS
        }

    def find_relevant(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedNote]:

        notes = list(
            self._db.scalars(
                select(Note).order_by(Note.updated_at.desc())
            )
        )

        if not notes:
            return []

        tokens = self._tokenize(query)

        note_query = bool(tokens & NOTE_QUERY_TERMS)
        recent_query = bool(tokens & RECENT_QUERY_TERMS)

        # Explicit note requests:
        # "show my notes"
        # "what notes do I have"
        if note_query and len(tokens) <= 5:
            return [
                self._convert(note)
                for note in notes[:limit]
            ]

        scored: list[tuple[int, datetime, Note]] = []

        for note in notes:

            title = note.title.lower()
            summary = note.summary.lower()
            content = note.content.lower()
            tags = " ".join(note.tags).lower()

            searchable = f"{title} {summary} {content} {tags}"

            score = 0

            for token in tokens:

                if token in title:
                    score += 10

                if token in summary:
                    score += 8

                if token in tags:
                    score += 6

                if token in content:
                    score += 5

                # Partial word match
                if any(token in word for word in searchable.split()):
                    score += 2

            # Boost newer notes when user asks about recent work
            if recent_query:
                score += 5

            if score > 0:
                scored.append(
                    (
                        score,
                        note.updated_at,
                        note,
                    )
                )

        scored.sort(
            key=lambda item: (item[0], item[1]),
            reverse=True,
        )

        return [
            self._convert(note)
            for _, _, note in scored[:limit]
        ]

    @staticmethod
    def _convert(note: Note) -> RetrievedNote:
        return RetrievedNote(
            id=note.id,
            title=note.title,
            summary=note.summary or "",
            content=note.content,
            tags=note.tags or [],
            created_at=note.created_at,
            updated_at=note.updated_at,
        )