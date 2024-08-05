import os

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langserve import add_routes

from .langc import BankAgent

class UserQuery(BaseModel):
    user_id: str
    full_name: str
    context: str
    question: str


app = FastAPI()


@app.post("/ask")
async def ask_assistant(query: UserQuery):
    assistant = BankAgent().contextualise(query.user_id, query.full_name, query.context).init()
    resp = await assistant.aprompt(query.question)
    return {"content": resp}

add_routes(app, RunnableLambda(ask_assistant))

