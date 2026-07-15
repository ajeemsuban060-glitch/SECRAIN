import { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChatWorkspace } from "./ChatWorkspace";
import { NotesWorkspace } from "./NotesWorkspace";
import "./styles.css";

function App() {
  const [section, setSection] = useState<"chat" | "notes">("chat");

  return <main className="app-shell"><aside><div className="brand">SECRAIN <span>Your second brain</span></div><nav className="primary-nav"><button type="button" className={section === "chat" ? "active" : ""} onClick={() => setSection("chat")}>Chat</button><button type="button" className={section === "notes" ? "active" : ""} onClick={() => setSection("notes")}>Notes</button></nav></aside>{section === "chat" ? <ChatWorkspace /> : <NotesWorkspace />}</main>;
}

createRoot(document.getElementById("root")!).render(<App />);
