from server.llm.ollama_client import OllamaClient, Message


def main() -> None:
    client = OllamaClient()
    messages = [
        Message(
            role="system",
            content="You are an expert technical support engineer. Respond to the question professionally.",
        ),
        Message(role="user", content="Hello, how are you?"),
    ]

    # The chat response from the LLM's chat API.
    print(client.chat(messages))

    # Prints one float array that represent the embedding of the input text,
    # using the LLM's embedding API.
    print(client.embed(["Hello, how are you?"]))


if __name__ == "__main__":
    main()
