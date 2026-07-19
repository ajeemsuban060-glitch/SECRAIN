<p align="center">
  <img src="assets/banner.png" alt="SECRAIN Banner" width="100%">
</p>

<h1 align="center">🧠 SECRAIN</h1>

<p align="center">
  <strong>Your Second Brain</strong><br>
  Local-First AI Productivity & Knowledge Management System
</p>

<p align="center">

![License](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)

![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black?style=for-the-badge)

</p>

---

> **SECRAIN** is a local-first AI productivity platform designed to become your permanent digital second brain.
>
> It remembers your knowledge, organizes your notes, retrieves context intelligently, and assists you using private, on-device AI.

---



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
