███████╗███████╗ ██████╗██████╗  █████╗ ██╗███╗   ██╗
██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██║████╗  ██║
███████╗█████╗  ██║     ██████╔╝███████║██║██╔██╗ ██║
╚════██║██╔══╝  ██║     ██╔══██╗██╔══██║██║██║╚██╗██║
███████║███████╗╚██████╗██║  ██║██║  ██║██║██║ ╚████║
╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

        


# 🧠 SECRAIN

> **Your Second Brain** --- A local-first AI productivity platform.

## 🌟 Vision

SECRAIN is a modular AI operating system focused on privacy, memory, and
productivity. It combines AI chat, persistent memory, notes, and future
knowledge modules into one local-first application.

## 🎯 Purpose

-   Build a true second brain
-   Keep user data local
-   Provide long-term memory
-   Deliver extensible, clean architecture

## 🏗 Architecture

``` mermaid
graph TD
User-->Frontend
Frontend-->FastAPI
FastAPI-->ChatService
FastAPI-->NotesService
ChatService-->NoteRetriever
NoteRetriever-->SQLite
ChatService-->Ollama
Ollama-->LocalLLM
```

## 🔄 Workflow

``` mermaid
flowchart TD
A[User]-->B[Frontend]
B-->C[API]
C-->D[Retrieve Notes]
D-->E[Conversation]
E-->F[Ollama]
F-->G[Response]
```

## 📁 Current Repository

``` text
SECRAIN/
├── backend/
│   ├── app/
│   ├── frontend/
│   ├── .venv/
│   └── ...
├── LICENSE
└── README.md
```

## ✅ Current Features

-   AI Chat
-   Persistent Conversations
-   Notes
-   Intelligent Note Retrieval
-   Ollama Integration
-   SQLite Storage

## 🚧 Planned

-   ChromaDB Semantic Memory
-   PDF Chat
-   Tasks
-   Dashboard
-   Voice Assistant

## ▶ Run

### Backend

``` bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

### Frontend

``` bash
cd backend/frontend
npm install
npm run dev
```

## 🤝 Contributing

Fork → Branch → Commit → Pull Request

## 📜 License

MIT

------------------------------------------------------------------------

**SECRAIN** aims to become a complete local AI operating
system---remembering, organizing, reasoning, and helping you build.
