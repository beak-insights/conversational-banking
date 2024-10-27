import os
import logging
from telegram import User
from httpx import AsyncClient, RequestError
from .session import get_session, update_session

logger = logging.getLogger(__name__)

BANK_API = os.getenv('BANK_API')
ASSISTANT_API = os.getenv('ASSISTANT_API')

print(BANK_API, ASSISTANT_API)

async def assistant_post(url, user: User, question: str):
    logger.info(f"user::{user}::")
    _user = user.full_name if user.full_name else user.username
    async with AsyncClient(base_url=ASSISTANT_API, timeout=30.0) as client:
        logger.info(f"bank_post::{_user}::: {client.base_url}{url}: question {question}")
        try:
            response = await client.post(
                url, 
                json={
                    "user_id": str(user.id), 
                    "full_name": _user,
                    "question": question
                }
            )
            return response.json()
        except RequestError:
            return {"content": "Assistant is currently not reachable. Please try again later."}

