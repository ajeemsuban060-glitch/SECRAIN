from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.notes.models import Note


class NotesRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list(self) -> list[Note]:
        return list(self._db.scalars(select(Note).order_by(Note.updated_at.desc())))

    def get(self, note_id: int) -> Note | None:
        return self._db.get(Note, note_id)

    def create(self, **values: object) -> Note:
        note = Note(**values)
        self._db.add(note)
        self._db.commit()
        self._db.refresh(note)
        return note

    def update(self, note: Note, **values: object) -> Note:
        for field, value in values.items():
            setattr(note, field, value)
        self._db.commit()
        self._db.refresh(note)
        return note
