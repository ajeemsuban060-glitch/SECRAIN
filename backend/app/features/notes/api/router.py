from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.ollama import OllamaUnavailableError
from app.database.session import get_db
from app.features.notes.schemas import CaptureAssistRequest, CaptureAssistResponse, NoteCreate, NoteRead, NoteUpdate
from app.features.notes.service import NoteNotFoundError, NotesService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)):
    return NotesService(db).list_notes()


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return NotesService(db).create_note(payload)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    try:
        return NotesService(db).get_note(note_id)
    except NoteNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    try:
        return NotesService(db).update_note(note_id, payload)
    except NoteNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")


@router.post("/assist-capture", response_model=CaptureAssistResponse)
async def assist_capture(payload: CaptureAssistRequest, db: Session = Depends(get_db)):
    try:
        return await NotesService(db).assist_capture(payload.content)
    except OllamaUnavailableError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))
