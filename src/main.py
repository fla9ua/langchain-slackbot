import os
from typing import Optional, List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_core.messages import HumanMessage, AIMessage

from tools import all_tools
from prompts.system_prompts import SYSTEM_PROMPT

def convert_history_to_messages(conversation_history: List[Dict[str, str]]) -> List:
    """Slack会話履歴をLangChainメッセージに変換"""
    messages = []
    for msg in conversation_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages

def chat_with_history():
    """Chat with history"""
    if not os.environ.get("MODEL_NAME"):
        raise ValueError("MODEL_NAME environment variable is not set")

    model = ChatOpenAI(
        model=os.environ.get("MODEL_NAME"),
        temperature=float(os.environ.get("MODEL_TEMPERATURE", "0")),
        request_timeout=float(os.environ.get("MODEL_TIMEOUT", "30")),
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", os.environ.get("SYSTEM_PROMPT", SYSTEM_PROMPT)),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(model, all_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        handle_parsing_errors=True,
        max_iterations=int(os.environ.get("MAX_AGENT_ITERATIONS", "3")),
    )

    class SlackThreadRunnable:
        def __init__(self, agent_executor):
            self.agent_executor = agent_executor

        def invoke(self, input_dict, config=None):
            # 会話履歴の取得と変換
            conversation_history = config.get("configurable", {}).get("conversation_history", [])
            history_messages = convert_history_to_messages(conversation_history)

            # 会話履歴を含めて実行
            return self.agent_executor.invoke(
                {
                    "user_input": input_dict["user_input"],
                    "history": history_messages,
                }
            )

    return SlackThreadRunnable(agent_executor)
