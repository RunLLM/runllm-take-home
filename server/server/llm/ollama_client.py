from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Literal, Optional, Sequence

from ollama import Client

LLM = "llama3.2:3b"
EMBEDDING = "nomic-embed-text"
NUM_DIMENSIONS = 768


@dataclass
class Message:
    role: Literal["user", "assistant", "system"]
    content: str


class OllamaClient:
    def __init__(self) -> None:
        self.client = Client(host="http://localhost:11434")

    def embed(self, inputs: List[str]) -> Sequence[Sequence[float]]:
        """Converts the given strings to their vector embeddings using the Ollama embedding API.

        These embeddings can be later used to query the VectorDB.
        """
        response = self.client.embed(model=EMBEDDING, input=inputs)
        return response.embeddings

    def chat(self, messages: List[Message], format: Optional[Dict[str, Any]] = None) -> str:
        """Sends the messages to the LLM and returns the string response."""
        response = self.client.chat(
            model=LLM,
            messages=[asdict(m) for m in messages],
            format=format,
        )
        assert response.message.content
        return response.message.content
