import os
import warnings
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

warnings.filterwarnings("ignore")
load_dotenv()

# --------------------------------------------------
# LLM (Gemini)
# --------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# --------------------------------------------------
# Prompt template (Customer Care behavior)
# --------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional customer care assistant for a mobile application.

Rules:
- Be polite, calm, and empathetic
- Give step-by-step guidance
- Ask for clarification only if required
- Never blame the customer
- If the issue is serious or unclear, suggest human support
"""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# --------------------------------------------------
# Session memory store
# --------------------------------------------------
_store = {}

def _get_session_history(session_id: str):
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]

# --------------------------------------------------
# Runnable agent with memory
# --------------------------------------------------
agent = RunnableWithMessageHistory(
    prompt | llm,
    _get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# ==================================================
# PUBLIC FUNCTION USED BY FLASK
# ==================================================

def handle_customer_message(message: str, session_id: str):
    """
    Handles a customer message and returns bot reply.
    """
    result = agent.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}}
    )
    return result.content
