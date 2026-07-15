import { FormEvent, useEffect, useState } from "react";

type Message = { id: number; role: "user" | "assistant"; content: string; created_at: string };
type Conversation = { id: number; title: string; created_at: string; updated_at: string; messages?: Message[] };
type NoteReference = { id: number; title: string };
const API_URL = "http://127.0.0.1:8000/api/chat";

export function ChatWorkspace() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [current, setCurrent] = useState<Conversation | null>(null);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [referencedNotes, setReferencedNotes] = useState<NoteReference[]>([]);

  const loadConversations = async () => {
    const response = await fetch(`${API_URL}/conversations`);
    if (response.ok) setConversations(await response.json());
  };
  const openConversation = async (id: number) => {
    setError("");
    setReferencedNotes([]);
    const response = await fetch(`${API_URL}/conversations/${id}`);
    if (response.ok) setCurrent(await response.json());
  };
  const newConversation = async (): Promise<Conversation | null> => {
    setError("");
    try {
      const response = await fetch(`${API_URL}/conversations`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      if (!response.ok) throw new Error("Could not create a conversation.");
      const conversation: Conversation = await response.json();
      setCurrent(conversation);
      await loadConversations();
      return conversation;
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not create a conversation.");
      return null;
    }
  };
  useEffect(() => { void loadConversations(); }, []);
  useEffect(() => { if (!current && conversations[0]) void openConversation(conversations[0].id); }, [conversations, current]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const content = text.trim();
    if (!content || busy) return;
    const conversation = current ?? await newConversation();
    if (!conversation) return;
    const optimistic: Message = { id: Date.now(), role: "user", content, created_at: new Date().toISOString() };
    setCurrent({ ...conversation, messages: [...(conversation.messages ?? []), optimistic] });
    setText(""); setBusy(true); setError("");
    try {
      const response = await fetch(`${API_URL}/conversations/${conversation.id}/messages`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "The message could not be sent.");
      setReferencedNotes(body.referenced_notes ?? []);
      await openConversation(conversation.id); await loadConversations();
    } catch (reason) { setError(reason instanceof Error ? reason.message : "The message could not be sent."); await openConversation(conversation.id); }
    finally { setBusy(false); }
  };

  return <section className="chat"><header><div><h1>{current?.title ?? "Start a conversation"}</h1><p>Private, local AI chat</p></div><span className="local">Local</span></header><div className="workspace-actions"><button type="button" className="new" onClick={() => void newConversation()}>+ New conversation</button><div className="item-list">{conversations.map(item => <button type="button" className={item.id === current?.id ? "active" : ""} key={item.id} onClick={() => void openConversation(item.id)}>{item.title}</button>)}</div></div><div className="messages">{!current?.messages?.length && <div className="empty"><h2>What is on your mind?</h2><p>SECRAIN runs through your local Ollama model. Your conversations stay on this device.</p></div>}{current?.messages?.map(message => <article key={message.id} className={message.role}><label>{message.role === "user" ? "You" : "SECRAIN"}</label><p>{message.content}</p></article>)}{busy && <article className="assistant"><label>SECRAIN</label><p className="thinking">Thinking...</p></article>}{referencedNotes.length > 0 && <p className="note-context">Used saved notes: {referencedNotes.map(note => note.title).join(", ")}</p>}</div>{error && <p className="error">{error}</p>}<form onSubmit={submit}><textarea value={text} onChange={event => setText(event.target.value)} placeholder="Message SECRAIN..." rows={2} disabled={busy}/><button type="submit" disabled={busy || !text.trim()}>{busy ? "Thinking" : "Send"}</button></form></section>;
}
