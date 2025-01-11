from langchain_community.tools import DuckDuckGoSearchRun
from vector import vector_to_tool
from typing import List
from langchain.tools import BaseTool
import os

def initialize_tools() -> List[BaseTool]:
    """Initialize tools based on environment variables"""
    tools = []
    
    # 検索ツール
    if os.environ.get("ENABLE_SEARCH", "true").lower() == "true":
        search_tool = DuckDuckGoSearchRun()
        search_tool.name = "web_search"
        tools.append(search_tool)
    
    # ベクトルツール
    if os.environ.get("ENABLE_VECTOR", "true").lower() == "true":
        vector_tool = vector_to_tool()
        vector_tool.name = "vector_search"
        tools.append(vector_tool)
    
    return tools

all_tools = initialize_tools()
