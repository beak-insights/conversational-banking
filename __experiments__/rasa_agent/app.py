import os

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

from .langc import BankAgent

sessions: dict[str, BankAgent] = {}

class UserQuery(BaseModel):
    user_id: str
    full_name: str
    context: str
    question: str

app = FastAPI()


@app.post("/ask")
async def ask_assistant(query: UserQuery):
    if query.user_id not in sessions:
        #1. maybe get context about user from bank using user id
        #2. create a new session
        sessions[query.user_id] = BankAgent().contextualise(
            query.user_id, query.full_name, query.context
        ).init()
    
    resp = await sessions[query.user_id].aprompt(query.question)
    return {"content": resp}

add_routes(app, RunnableLambda(ask_assistant))

