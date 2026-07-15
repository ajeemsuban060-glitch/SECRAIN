import { useEffect, useState } from "react";

type Note = { id: number; title: string; content: string; summary: string; tags: string[]; updated_at: string };
type Draft = Omit<Note, "id" | "updated_at">;
const EMPTY_DRAFT: Draft = { title: "", content: "", summary: "", tags: [] };
const API_URL = "http://127.0.0.1:8000/api/notes";

export function NotesWorkspace() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT);
  const [tagsText, setTagsText] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  const loadNotes = async () => {
    const response = await fetch(API_URL);
    if (response.ok) setNotes(await response.json());
  };
  const selectNote = async (id: number) => {
    const response = await fetch(`${API_URL}/${id}`);
    if (!response.ok) return setMessage("Could not open this note.");
    const note: Note = await response.json();
    setSelectedId(note.id); setDraft(note); setTagsText(note.tags.join(", ")); setMessage("");
  };
  const newNote = () => { setSelectedId(null); setDraft(EMPTY_DRAFT); setTagsText(""); setMessage(""); };
  useEffect(() => { void loadNotes(); }, []);

  const tags = () => tagsText.split(",").map(tag => tag.trim().toLowerCase()).filter(Boolean).slice(0, 10);
  const save = async () => {
    if (!draft.title.trim() && !draft.content.trim()) return setMessage("Add a title or some note content before saving.");
    setBusy(true); setMessage("");
    const payload = { ...draft, title: draft.title.trim() || "Untitled note", tags: tags() };
    try {
      const response = await fetch(selectedId ? `${API_URL}/${selectedId}` : API_URL, { method: selectedId ? "PATCH" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Could not save the note.");
      setSelectedId(body.id); setDraft(body); setTagsText(body.tags.join(", ")); setMessage("Saved locally."); await loadNotes();
    } catch (reason) { setMessage(reason instanceof Error ? reason.message : "Could not save the note."); }
    finally { setBusy(false); }
  };
  const assist = async () => {
    if (!draft.content.trim()) return setMessage("Write or paste note content before using AI assist.");
    setBusy(true); setMessage("");
    try {
      const response = await fetch(`${API_URL}/assist-capture`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content: draft.content }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "AI assistance is unavailable.");
      setDraft(current => ({ ...current, title: body.title || current.title, summary: body.summary || current.summary, tags: body.tags })); setTagsText(body.tags.join(", ")); setMessage("Suggestions applied. Review and save when ready.");
    } catch (reason) { setMessage(reason instanceof Error ? reason.message : "AI assistance is unavailable."); }
    finally { setBusy(false); }
  };

  return <section className="notes"><header><div><h1>{selectedId ? "Edit note" : "Capture a note"}</h1><p>Private notes, saved on this device.</p></div><button type="button" className="new" onClick={newNote}>+ New note</button></header><div className="notes-layout"><div className="note-list">{notes.length === 0 && <p className="muted">No saved notes yet.</p>}{notes.map(note => <button type="button" key={note.id} className={note.id === selectedId ? "active" : ""} onClick={() => void selectNote(note.id)}><strong>{note.title}</strong><span>{note.summary || note.content.slice(0, 60) || "Empty note"}</span></button>)}</div><div className="note-editor"><label>Title<input value={draft.title} onChange={event => setDraft({ ...draft, title: event.target.value })} placeholder="A clear title" /></label><label>Note<textarea value={draft.content} onChange={event => setDraft({ ...draft, content: event.target.value })} placeholder="Capture an idea, meeting detail, or anything worth remembering..." rows={11} /></label><label>Summary<input value={draft.summary} onChange={event => setDraft({ ...draft, summary: event.target.value })} placeholder="Optional short summary" /></label><label>Tags<input value={tagsText} onChange={event => setTagsText(event.target.value)} placeholder="work, ideas, research" /></label>{message && <p className={message.includes("Could") || message.includes("unavailable") ? "error" : "notice"}>{message}</p>}<div className="note-actions"><button type="button" className="secondary" onClick={() => void assist()} disabled={busy || !draft.content.trim()}>AI organize</button><button type="button" onClick={() => void save()} disabled={busy}>{busy ? "Working..." : "Save note"}</button></div></div></div></section>;
}
