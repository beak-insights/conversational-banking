import logging
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

from .langc import BankAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

sessions: dict[str, BankAgent] = {}

class UserQuery(BaseModel):
    user_id: str
    question: str

app = FastAPI()


@app.post("/ask")
async def ask_assistant(query: UserQuery):
    if query.user_id not in sessions:
        logger.info(f"User does not exist in session:  contextualising ...")
        with_context = await BankAgent().contextualise(
            query.user_id
        )
        logger.info(f"Applying context ...")
        sessions[query.user_id] = with_context.init()
        logger.info(f"Context Applied ...")
    
    logger.info(f"Sending query to assistant ... from {sessions[query.user_id].user_id}")
    resp = await sessions[query.user_id].aprompt(query.question)
    logger.info(f"Received response from assistant")
    return {"content": resp}

add_routes(app, RunnableLambda(ask_assistant))

