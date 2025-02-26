from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Literal, Optional, Sequence

import requests
from ollama import Client

from server.api_key import API_KEY

EMBEDDING = "nomic-embed-text"
NUM_DIMENSIONS = 768
OLLAMA_HOST = "https://runllm-interview-ollama-24235262657.us-central1.run.app"
RUNLLM_HOST = "https://runllm-interview-gpt-24235262657.us-central1.run.app"


@dataclass
class Message:
    role: Literal["user", "assistant", "system"]
    content: str


class OllamaClient:
    def __init__(self) -> None:
        if not API_KEY:
            raise ValueError("API_KEY is not set. Please set the API_KEY provided by RunLLM.")
        self.api_key = API_KEY
        self.ollama_client = Client(host=OLLAMA_HOST)

    def embed(self, inputs: List[str]) -> Sequence[Sequence[float]]:
        """Converts the given strings to their vector embeddings using the Ollama embedding API.

        These embeddings can be later used to query the VectorDB.
        """
        response = self.ollama_client.embed(model=EMBEDDING, input=inputs)
        return response.embeddings

    def chat(self, messages: List[Message], format: Optional[Dict[str, Any]] = None) -> str:
        """Sends the messages to the LLM and returns the string response."""
        response = requests.post(
            url=RUNLLM_HOST,
            json={
                "api_key": self.api_key,
                "messages": [asdict(m) for m in messages],
                "json_mode": bool(format),
            },
        )
        obj = response.json()
        assert "choices" in obj
        return obj["choices"][0]
