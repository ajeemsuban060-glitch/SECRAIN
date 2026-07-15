from collections.abc import Sequence

from ollama import AsyncClient, ResponseError

from app.ai.provider import ChatTurn
from app.core.config import settings


class OllamaUnavailableError(RuntimeError):
    """Raised when Ollama or its configured model cannot serve a request."""


class OllamaProvider:
    def __init__(self) -> None:
        self._client = AsyncClient(host=settings.OLLAMA_HOST)

    async def respond(self, messages: Sequence[ChatTurn]) -> str:
        try:
            response = await self._client.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{"role": turn.role, "content": turn.content} for turn in messages],
            )
        except (ResponseError, OSError) as error:
            raise OllamaUnavailableError(
                f"Unable to reach Ollama using model '{settings.OLLAMA_MODEL}'. "
                "Start Ollama and ensure the model is installed."
            ) from error

        content = response.message.content.strip()
        if not content:
            raise OllamaUnavailableError("Ollama returned an empty response.")
        return content
