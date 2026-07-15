# Local AI Chat Slice

## Objective

Provide a private chat workflow that persists conversations locally and sends only the conversation context to a locally running Ollama model.

## Architecture

`frontend` calls the FastAPI chat routes. The chat service stores messages in SQLite, then asks the `LanguageModelProvider` interface for an answer. The initial adapter is `OllamaProvider`; future local or hosted providers can implement the same interface without changing the chat feature.

## Run locally

1. Install and start Ollama, then make the configured model available: `ollama pull qwen3:8b`.
2. From `backend`, start the API with `./.venv/Scripts/python.exe run.py`.
3. From `backend/frontend`, install dependencies once with `npm.cmd install`, then start the interface with `npm.cmd run dev`.
4. Open the URL shown by Vite (normally `http://127.0.0.1:5173`).

The backend configuration is in `.env`. `OLLAMA_MODEL`, `OLLAMA_HOST`, and `FRONTEND_ORIGIN` can be adjusted for a different local setup.

## API

- `GET /api/chat/conversations` lists saved conversations.
- `POST /api/chat/conversations` creates a conversation.
- `GET /api/chat/conversations/{id}` returns a conversation with messages.
- `POST /api/chat/conversations/{id}/messages` saves a user message and returns the local model's response.

If Ollama is unavailable or its configured model is missing, sending a message returns HTTP 503 with an actionable message; existing saved conversations remain available.
