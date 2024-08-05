import os
import bs4
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver

from .tools import (
   lc_balance, lc_withdraw, lc_external_transfer, lc_internal_transfer, lc_deposit, lc_statement
)


BASE_SYSTEM_PROMPT = ("You are a Bank Assistant that handles and manages customer queries."
"If you are greeted, always respond with a greeting adressing them with their full name"
"You will be interacting with customers who have queries related to their bank accound the bank's services." 
"If the user wants to conduct a transaction, before the transaction, always ask the user if they would like to proceed with the transaction or not."
"Customers may request to check their bank account(s) balances, bank statements, conduct transfers, and withdraw money."
"You have access to the customer's transaction history and the details associated with each transaction."
"Do not use phrases like 'based on my knowledge' or 'depending on the information'."
"If a customer needs further assistance related to the bank services, be ready to provide it."
"You shall not answer any question based on your own knowledge or experience."
"Only answer bank related questions!!. Any question outside the banking context and its services say sorry i cant help you with this query."
"Answer questions using the necessary provided tools otherwise say you don't know."
"When you need to use a tool, makesure you have the required parameters to use the tool, if not ask the user for the required parameters."
"Below are the details of the user that you are engaging with:\n\n"
"{user_details}\n"
"{extra_more}"
)


class BankAgent:

    def __init__(self):
        self.system_prompt = BASE_SYSTEM_PROMPT
        self.model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.user_id = None
        self.full_name = None

    async def aprompt(self, query: str):
        return (await self.executor.ainvoke(
            {
                "messages": [HumanMessage(content=query)]}, 
                config={"configurable": {"thread_id": self.user_id}
            }
        ))["messages"][-1].content

    def prompt(self, query: str):
        return self.executor.invoke(
            {
                "messages": [HumanMessage(content=query)]}, 
                config={"configurable": {"thread_id": self.user_id}
            }
        )["messages"][-1].content

    def init(self):
        if not self.user_id or not self.full_name:
            raise ValueError("User context not set")
        
        self.executor = self._create_agent()
        return self
    
    def contextualise(self, user_id: str, full_name: str, extra_context):
        self.user_id = user_id
        self.full_name = full_name
        self.system_prompt = BASE_SYSTEM_PROMPT.format(
            user_details=f"User ID: {str(user_id)}, Full Name: {full_name}",
            extra_more=extra_context
        )
        return self
    
    def _create_retriever(self):
        loader = WebBaseLoader(
            web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        retriever = vectorstore.as_retriever()
        return retriever
    
    def _create_tools(self):
        lc_knowledgebase = create_retriever_tool(
            self._create_retriever(),
            "blog_post_retriever",
            "Searches and returns excerpts from the Autonomous Agents blog post.",
        )
        return [
            lc_knowledgebase, lc_balance, lc_deposit, lc_withdraw, 
            lc_external_transfer, lc_internal_transfer, lc_statement
        ]

    def _create_agent(self):
        tools = self._create_tools()
        memory = AsyncSqliteSaver.from_conn_string(":memory:")
        agent_executor = create_react_agent(
            self.model, tools, checkpointer=memory, 
            messages_modifier=SystemMessage(content=self.system_prompt)
        )
        return agent_executor
