import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

from.prompts import SYSTEM_PROMPT

model = ChatOpenAI(model="gpt-3.5-turbo")
store = {}
config = {"configurable": {"session_id": "amuse1234"}}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        store[session_id].add_message(SystemMessage(SYSTEM_PROMPT))
    return store[session_id]

llm_chain = RunnableWithMessageHistory(model, get_session_history)


def lcprompt(input):
    response = llm_chain.invoke(
        [HumanMessage(content=input)],
        config=config,
    )
    print(response.content +"\n")