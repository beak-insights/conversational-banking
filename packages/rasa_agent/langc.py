import os
from typing import List, Dict, Any

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver

from .tools import (
    lc_balance, lc_withdraw, lc_external_transfer,
    lc_internal_transfer, lc_deposit, lc_statement
)
from .prompts import BASE_SYSTEM_PROMPT

class BankAgent:
    def __init__(self):
        self.system_prompt = BASE_SYSTEM_PROMPT
        self.model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.user_id = None
        self.full_name = None
        self.executor = None

    async def aprompt(self, query: str) -> str:
        response = await self.executor.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": self.user_id}}
        )
        return response["messages"][-1].content

    def prompt(self, query: str) -> str:
        response = self.executor.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": self.user_id}}
        )
        return response["messages"][-1].content

    def init(self) -> 'BankAgent':
        if not self.user_id or not self.full_name:
            raise ValueError("User context not set")
        self.executor = self._create_agent()
        return self

    def contextualise(self, user_id: str, full_name: str, extra_context: str) -> 'BankAgent':
        self.user_id = user_id
        self.full_name = full_name
        self.system_prompt = BASE_SYSTEM_PROMPT.format(
            user_details=f"User ID: {user_id}, Full Name: {full_name}",
            extra_more=extra_context
        )
        return self

    def _create_retriever(self):
        loader = DirectoryLoader("./", glob="**/*.md", loader_cls=TextLoader)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        vectorstore = Chroma.from_documents(
            documents=text_splitter.split_documents(docs),
            embedding=OpenAIEmbeddings()
        )
        return vectorstore.as_retriever()

    def _create_tools(self) -> List[Dict[str, Any]]:
        lc_knowledgebase = create_retriever_tool(
            self._create_retriever(),
            "bank_knowledge_retriever",
            "Searches and returns relevant information from the bank knowledge base"
        )
        return [
            lc_knowledgebase, lc_balance, lc_deposit, lc_withdraw,
            lc_external_transfer, lc_internal_transfer, lc_statement
        ]

    def _create_agent(self):
        tools = self._create_tools()
        memory = AsyncSqliteSaver.from_conn_string(":memory:")
        return create_react_agent(
            self.model,
            tools,
            checkpointer=memory,
            messages_modifier=SystemMessage(content=self.system_prompt)
        )