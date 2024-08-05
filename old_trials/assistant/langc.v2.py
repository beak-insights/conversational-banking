import os

from textwrap import dedent
import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from banking.api_lc import (
   lc_balance, lc_withdraw
)


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

BASE_SYSTEM_PROMPT = dedent("""You are a Bank Assistant that handles and manages customer queries. 
You will be interacting with customers who have queries related to their bank accound the bank's services. 
If the user wants to conduct a transaction, before the transaction, always ask the user if they would like to proceed with the transaction or not.
Customers may request to check their bank account(s) balances, bank statements, conduct transfers, and withdraw money.
You have access to the customer's transaction history and the details associated with each transaction.
Do not use phrases like 'based on my knowledge' or 'depending on the information'.
If a customer needs further assistance related to the bank services, be ready to provide it.
You shall not answer any question based on your own knowledge or experience.
Only answer bank related questions!!. Any question outside the banking context and its services say sorry i cant help you with this query.
Answer questions using the necessary provides tools otherwise say you don't know.
""")

# 1. Load, chunk and index the contents of the blog to create a retriever.
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


### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

### Answer question ###
system_prompt = (
    f"{BASE_SYSTEM_PROMPT}"
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Keep the answer short and concise."
    "\n\n"
    "{context}"
)


qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

con_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


def lcprompt(input):
    response = con_rag_chain.invoke(
        {"input": input}, 
        config={
            "configurable": {"session_id": "abc123"}
        }
    )
    print(response["answer"] +"\n")

##### Create an Agent #####
tool = create_retriever_tool(
    retriever,
    "blog_post_retriever",
    "Searches and returns excerpts from the Autonomous Agents blog post.",
)
tools = [tool, lc_balance, lc_withdraw]
memory = SqliteSaver.from_conn_string(":memory:")
agent_executor = create_react_agent(model, tools, checkpointer=memory, messages_modifier=SystemMessage(content=BASE_SYSTEM_PROMPT))


def agprompt(input, user_id: str):
    response = agent_executor.invoke(
        {
            "messages": [HumanMessage(content=input)]}, 
            config={"configurable": {"thread_id": user_id}
        }
    )
    output = response["messages"][-1].content
    print(output +"\n")
    return output


class BankAgent:
    def __init__(self):