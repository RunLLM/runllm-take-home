import json
import requests
from typing import List, Tuple

from pydantic import BaseModel

from server.api.chat import ChatResponse
from server.llm.ollama_client import OllamaClient

from tests.llm_judge import score_answer

MAX_DATA_SOURCES_FETCHED = 5


class TestCaseExpectation(BaseModel):
    answer: str
    data_source_ids: List[str]


def _send_server_request(message: str) -> ChatResponse:
    response = requests.post(
        "http://127.0.0.1:5001/api/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"message": message})
    )
    response.raise_for_status()
    return ChatResponse(**response.json())


def test_question_answers() -> None:
    """For every question, the endpoint is expected to return:
    1) The appropriate data source ids present in the Expectation.
    2) A reasonable answer using the data sources.
    """
    test_cases: List[Tuple[str, TestCaseExpectation]] = [
        (
            "How do I create an MLFlow AI gateway completion endpoint?",
            TestCaseExpectation(
                answer="Use the following command to create an endpoint: `mlflow gateway start --config-path config.yaml --port 7000`",
                data_source_ids=["4c1537cf4294593f8498a4b3ec9ad8f9"],
            )
        ),
        (
            "What method do I use to log an artifact of an LLM run?",
            TestCaseExpectation(
                answer="Use the `mlflow.log_artifact` method.",
                data_source_ids=["85ac83c0095a952f9f8ebc2b762f7659"],
            )
        ),
    ]

    llm_client = OllamaClient()
    for i, (question, expectation) in enumerate(test_cases):
        print(f"Running test case {i+1}/{len(test_cases)}")
        chat_resp = _send_server_request(question)

        assert (
            len(chat_resp.data_source_ids) <= MAX_DATA_SOURCES_FETCHED
        ), f"Fetched too many data source entries for the question. Max allowed: {MAX_DATA_SOURCES_FETCHED}"

        for expected_ds_ids in expectation.data_source_ids:
            # Check that all expected data source ids were fetched.
            assert (
                all(expected_ds_id in chat_resp.data_source_ids for expected_ds_id in expectation.data_source_ids)
            ), f"Not all expected data source ids are present in the response.\nExpected {expected_ds_ids}\nGot {chat_resp.data_source_ids}"

            # Check that the answer was reasonable.
            score = score_answer(
                llm_client, question, expectation.answer, chat_resp.message
            )
            assert (
                score.score >= 2
            ), f"Answer was not reasonable. Reason: {score.reason}"