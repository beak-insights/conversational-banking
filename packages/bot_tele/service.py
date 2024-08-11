import os
import logging
from telegram import User
from httpx import AsyncClient, RequestError
from .session import get_session, update_session

logger = logging.getLogger(__name__)

BANK_API = os.getenv('BANK_API')
ASSISTANT_API = os.getenv('ASSISTANT_API')

print(BANK_API, ASSISTANT_API)


async def _ask_context(user: User, question: str) -> dict:
    return {
        **(await get_session(user)),
        "question": question
    }


async def bank_post(url, data):
    async with AsyncClient(base_url=BANK_API, timeout=30.0) as client:
        try:
            response = await client.post(url, json=data)
            return response.json()
        except RequestError:
            return {"content": "Bank API is currently not reachable. Please try again later."}

async def assistant_post(url, user: User, question: str):
    data = await _ask_context(user, question)
    if not data["context"] or data["context"] is None:
        resp = await bank_post("/seed", {"user_id": str(user.id), "full_name": user.full_name})
        await update_session(user, user_context=resp["content"])
        data = await _ask_context(user, question)
    
    logger.info(f"assistant_post data {data}")
    async with AsyncClient(base_url=ASSISTANT_API, timeout=30.0) as client:
        logger.info(f"bank_post: {client.base_url}{url}: data {data}")
        try:
            response = await client.post(url, json=data)
            return response.json()
        except RequestError:
            return {"content": "Assistant is currently not reachable. Please try again later."}
    
