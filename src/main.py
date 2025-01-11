import os
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import (
    InMemoryChatMessageHistory,
    DynamoDBChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from tools import all_tools
from prompts.system_prompts import SYSTEM_PROMPT

store = {}

def chat_with_history():
    """Chat with history"""
    model = ChatOpenAI(model=os.environ.get("MODEL_NAME"), temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(model, all_tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=all_tools)

    runnable_agent = RunnableWithMessageHistory(
        runnable=agent_executor,
        get_session_history=_get_session_history,
        input_messages_key="user_input",
        history_messages_key="history",
    )

    return runnable_agent


def _get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Store and retrieve session history in local memory"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
