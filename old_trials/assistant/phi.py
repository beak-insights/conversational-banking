#!pip install phidata
#!pip install ollama
#!pip install groq
#!pip install duckduckgo-search
#!pip install markdown


from typing import Optional
from textwrap import dedent
from typing import Any, List

from phi.assistant import Assistant
from phi.llm.ollama import Ollama, OllamaTools
from phi.llm.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
import markdown


def get_local_bank_assistant(
    llm_provider: str = "groq",
    llm_model: str = None,
    tools: list = None,
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Assistant:
    """Get a Local Autonomous Banking Assistant."""
    
    if llm_provider == "groq":
        import os 
        os.environ["GROQ_API_KEY"] = ""
        llm = Groq(model=llm_model)
    elif llm_provider == "ollama":
        llm = OllamaTools(model=llm_model)


    # Team
    bank_teller = Assistant(
        name="Bank Teller",
        llm=llm,
        role="Process account transactions and pay utility bills.",
        tools=tools,
        description="You are a Bank Teller tasked with processing user transactions on their bank accounts.",
        instructions=[
            "The Receptionist will provide you with requests that you need to fulfill.",
            "Transfer money for the customer to the required accounts.",
            "Pay utility bills for the customer.",
        ],
        debug_mode=debug_mode,
    )
    account_manager = Assistant(
        name="Account Manager",
        llm=llm,
        role="Manage account information including balance inquiries and statements.",
        tools=tools,
        description="You are an Account Manager tasked with managing user questions on their bank account.",
        instructions=[
            "The Receptionist will provide you with requests that you need to fulfill.",
            "Get the current account balance.",
            "Retrieve bank statements.",
            "Reply in a simple manner targeting mobile chatting.",
            "Let the Receptionist know your response.",
        ],
        debug_mode=debug_mode,
    )
    general_inquiry_agent = Assistant(
        name="General Inquiry Agent",
        llm=llm,
        role="Handle general customer queries about bank processes and services.",
        description="You are a General Inquiry Agent tasked with providing information about bank services.",
        instructions=[
            "You will provide valuable information to the customer which is short and precise.",
            "You will interact with the Account Manager and Bank Teller for specific queries.",
            "For generic questions, directly respond with the answer.",
        ],
        debug_mode=debug_mode,
    )


    assistant = Assistant(
        name="local_bank_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=llm,
        tools=tools,
        #team=[bank_teller, account_manager, general_inquiry_agent],
        use_tools=True,
        show_tool_calls=False,
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
        description="You are a 'Bank Assistant' and your task is to help handle the Bank's customer queries.",
        introduction=dedent("""
            You are a Fintech bot that handles and manages customer transactions. 
            You will be interacting with customers who have queries related to their financial transactions. 
            If the user wants to retry the transaction, before retrying payment, always ask the user if they would like to proceed with the transaction or not.
        """),
        instructions=[
            "You are available 24/7 to assist customers with their transaction inquiries.",
            "Customers may request to check the status of their failed transactions, refunds, or payment statuses.",
            "You have access to the customer's transaction history and the details associated with each transaction.",
            "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
            "If a customer needs further assistance related to fintech bot functionalities or other related queries, be ready to provide it.",
        ],  
    )
    return assistant


session_state = dict()
session_state["assistant"] = None

llm_provider = "ollama"
llm_name = "llama3:instruct"
assistant_debug = True

def restart_llm(provider, llm, tools, debug_mode):
    # Get the assistant
    session_state["assistant"] = get_local_bank_assistant(
        provider,
        llm_model=llm,
        tools=tools,
        debug_mode=debug_mode
    )
    # Load existing messages
    assistant_chat_history = session_state["assistant"].memory.get_chat_history()
    if len(assistant_chat_history) > 0:
        print("Loading chat history ...")
        session_state["messages"] = assistant_chat_history
    else:
        print("No chat history found.")
        session_state["messages"] = [{"role": "assistant", "content": "Ask me questions..."}]


def prompt(q):
    session_state["messages"].append({"role": "user", "content": q})
    response = ""
    for delta in session_state["assistant"].run(q, stream=False):
        response += delta  # type: ignore
        markdown.markdown(response)
    # response = session_state["assistant"].print_response(q, markdown=True, stream=False)
    session_state["messages"].append({"role": "assistant", "content": response})
    print(response)


