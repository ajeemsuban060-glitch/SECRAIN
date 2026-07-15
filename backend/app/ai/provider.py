from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ChatTurn:
    role: str
    content: str


class LanguageModelProvider(Protocol):
    async def respond(self, messages: Sequence[ChatTurn]) -> str:
        """Return the model's response to a conversation."""
