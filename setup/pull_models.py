from server.llm.ollama_client import EMBEDDING, LLM, OllamaClient

def pull_models(client: OllamaClient) -> None:
    """Pulls the specified models using the provided client."""
    for model in [LLM, EMBEDDING]:
        print(f"Pulling model {model}")
        client.client.pull(model=model)

def main() -> None:
    client = OllamaClient()
    pull_models(client)

if __name__ == "__main__":
    main()
