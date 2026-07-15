# Notes with AI-assisted capture

## Objective

Give users a private place to capture and organize information before it becomes searchable long-term knowledge.

## Architecture

The Notes feature owns its SQLite `notes` table, API routes, service, and UI workspace. It uses the shared `LanguageModelProvider` abstraction only for the optional capture assist. The assist produces suggestions in memory; the user reviews them and explicitly saves the note.

## What it includes

- Create, view, and update locally persisted notes.
- Store title, content, summary, and tags.
- Ask the local Ollama model to suggest a title, concise summary, and up to five tags.
- Review AI suggestions before saving.

## API

- `GET /api/notes` lists notes, newest first.
- `POST /api/notes` creates a note.
- `GET /api/notes/{id}` retrieves a note.
- `PATCH /api/notes/{id}` updates a note.
- `POST /api/notes/assist-capture` returns AI suggestions without persisting them.

The next memory slice can add embeddings and retrieval as a separate concern, using saved notes as one knowledge source.
