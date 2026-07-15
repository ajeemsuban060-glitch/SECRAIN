import re
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.notes.models import Note

_STOP_WORDS = {"a", "an", "and", "are", "can", "do", "for", "how", "i", "in", "is", "it", "me", "my", "of", "on", "the", "to", "what", "with", "you"}
_PLANNING_TERMS = {"agenda", "plan", "priority", "priorities", "task", "tasks", "today", "tomorrow", "work"}


@dataclass(frozen=True)
class RetrievedNote:
    id: int
    title: str
    summary: str
    tags: list[str]

    def as_context(self) -> str:
        details = self.summary or "No summary available."
        tag_text = ", ".join(self.tags) or "none"
        return f"Title: {self.title}\nSummary: {details}\nTags: {tag_text}"


class NoteRetriever:
    """A deterministic local retriever until vector search is introduced."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def find_relevant(self, query: str, limit: int = 3) -> list[RetrievedNote]:
        notes = list(self._db.scalars(select(Note).order_by(Note.updated_at.desc())))
        tokens = {token for token in re.findall(r"[a-z0-9]+", query.lower()) if len(token) > 1 and token not in _STOP_WORDS}
        planning_query = bool(tokens & _PLANNING_TERMS)
        scored: list[tuple[int, int, Note]] = []
        for position, note in enumerate(notes):
            title = note.title.lower()
            summary = note.summary.lower()
            content = note.content.lower()
            tags = " ".join(note.tags).lower()
            score = sum(
                5 * (token in title) + 3 * (token in summary) + 4 * (token in tags) + (token in content)
                for token in tokens
            )
            if score or (planning_query and position < limit):
                scored.append((score, -position, note))

        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [
            RetrievedNote(id=note.id, title=note.title, summary=note.summary or note.content[:1_000], tags=note.tags)
            for _, _, note in scored[:limit]
        ]
