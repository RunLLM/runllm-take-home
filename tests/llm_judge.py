import json
from typing import List, Tuple

from pydantic import BaseModel

from server.llm.ollama_client import OllamaClient, Message

SYSTEM_PROMPT = """You are an impartial judge providing accurate quantitative evaluation for a response to a question. You are given a question, a reference, and a response. They are provided by in a markdown format. Your job is to evaluate the correctness of the response with respect to the reference. Following these guidelines, provide a integer score on a scale of 1 to 3, and also provide reasons for your scoring:

    Score 1: The response is completely wrong.
    Score 2: The response is partially correct.
    Score 3: The response is correct.
    
Respond with a json object with two fields, "score" and "reason"."""


class Score(BaseModel):
    score: int
    reason: str


def score_answer(
    client: OllamaClient, question: str, reference_answer: str, response: str
) -> Score:
    messages = [
        Message(role="system", content=SYSTEM_PROMPT),
        Message(
            role="user",
            content=f"#Question: {question}\n\n#Reference: {reference_answer}\n\n#Response: {response}",
        ),
    ]
    response_content = client.chat(messages, format=Score.model_json_schema())
    return Score.model_validate_json(response_content)

def score_answers(responses: List[Tuple[str, str, str]]) -> List[Score]:
    return [
        score_answer(OllamaClient(), question, reference_answer, response)
        for question, reference_answer, response in responses
    ]


if __name__ == "__main__":
    responses = [
        (
            "What is the capital of France?",
            "Paris",
            "The capital of France is Paris.",
        ),
        (
            "How to fly a unicorn with RunLLM",
            """To fly a unicorn with RunLLM, you need to follow these steps:
1. Purchase a saddle from runllm.com.
2. Purchase a unicorn from runllm.com.
3. Run `runllm install saddle --unicorn`.
4. Fly the unicorn with RunLLM.""",
            "There's no way to fly a unicorn with RunLLM.",
        ),
    ]
    print(score_answers(responses))
