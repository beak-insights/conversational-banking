import os
from telegram import User
from httpx import AsyncClient
from .session import get_session

BANK_API = os.getenv('BANK_API')
ASSISTANT_API = os.getenv('ASSISTANT_API')

print(BANK_API, ASSISTANT_API)


async def _ask_context(user: User, question: str) -> dict:
    return {
        **(await get_session(user)),
        "question": question
    }

async def assistant_post(url, user: User, question: str):
    data = await _ask_context(user, question)
    async with AsyncClient(base_url=ASSISTANT_API) as client:
        response = await client.post(url, data=data)
        return response.json()
    

async def bank_post(url, data):
    async with AsyncClient(base_url=BANK_API) as client:
        response = await client.post(url, data=data)
        return response.json()