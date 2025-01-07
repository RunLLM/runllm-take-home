import uuid
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from server.kvs.kvs import KVS

router = APIRouter(prefix="/api")
session_store = KVS()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    data_source_ids: List[str]


@router.post("/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    """This is a mock implementation of the chat endpoint, hard-coded to return a specific chat response."""

    chat_id = uuid.uuid4().hex
    response = "example response"
    data_source_ids = [
        "9a6584e4041f69a91fb4d0445eb997e3",
        "f1f051ca587dcdccce3cac1ecf442cc7",
        "59cb0b50d17febda2430502dd4722c40",
    ]

    session_store.put(
        chat_id,
        {"messages": [req.message, response], "data_source_ids": data_source_ids},
    )
    return ChatResponse(message=response, data_source_ids=data_source_ids)
