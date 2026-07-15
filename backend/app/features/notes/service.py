import json
from collections.abc import Mapping

from sqlalchemy.orm import Session

from app.ai.ollama import OllamaProvider
from app.ai.provider import ChatTurn, LanguageModelProvider
from app.features.notes.models import Note
from app.features.notes.repository import NotesRepository
from app.features.notes.schemas import CaptureAssistResponse, NoteCreate, NoteUpdate


class NoteNotFoundError(LookupError):
    pass


class NotesService:
    def __init__(self, db: Session, provider: LanguageModelProvider | None = None) -> None:
        self._repository = NotesRepository(db)
        self._provider = provider or OllamaProvider()

    def list_notes(self) -> list[Note]:
        return self._repository.list()

    def get_note(self, note_id: int) -> Note:
        note = self._repository.get(note_id)
        if note is None:
            raise NoteNotFoundError
        return note

    def create_note(self, payload: NoteCreate) -> Note:
        return self._repository.create(**payload.model_dump())

    def update_note(self, note_id: int, payload: NoteUpdate) -> Note:
        note = self.get_note(note_id)
        return self._repository.update(note, **payload.model_dump(exclude_unset=True))

    async def assist_capture(self, content: str) -> CaptureAssistResponse:
        prompt = (
            "Organize this personal note. Return JSON only, with keys title, summary, and tags. "
            "Use a short descriptive title, a 1-2 sentence summary, and at most 5 concise lowercase tags.\n\n"
            f"NOTE:\n{content}"
        )
        response = await self._provider.respond([ChatTurn(role="user", content=prompt)])
        return self._parse_assistance(response, content)

    @staticmethod
    def _parse_assistance(response: str, source: str) -> CaptureAssistResponse:
        cleaned = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            result = {}

        title = result.get("title") if isinstance(result, Mapping) else None
        summary = result.get("summary") if isinstance(result, Mapping) else None
        tags = result.get("tags") if isinstance(result, Mapping) else None
        fallback_title = next((line.strip() for line in source.splitlines() if line.strip()), "Untitled note")[:255]
        return CaptureAssistResponse(
            title=title.strip()[:255] if isinstance(title, str) and title.strip() else fallback_title,
            summary=summary.strip()[:2_000] if isinstance(summary, str) else "",
            tags=[tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()][:5] if isinstance(tags, list) else [],
        )
