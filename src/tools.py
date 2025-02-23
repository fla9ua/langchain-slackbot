import os
import logging
from typing import List
from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from vector import vector_to_tool

logger = logging.getLogger(__name__)

class ToolInitializationError(Exception):
    """ツール初期化エラー"""
    pass

def create_search_tool() -> BaseTool:
    """Web検索ツールの作成"""
    try:
        search_tool = DuckDuckGoSearchRun(
            max_retries=int(os.environ.get("SEARCH_MAX_RETRIES", "3"))
        )
        search_tool.name = "web_search"
        search_tool.description = "インターネット上の最新情報を検索する際に使用します。一般的な質問や最新のトピックに関する情報を提供できます。"
        return search_tool
    except Exception as e:
        logger.error(f"Failed to create search tool: {str(e)}", exc_info=True)
        raise ToolInitializationError(f"Search tool initialization failed: {str(e)}")

def create_vector_tool() -> BaseTool:
    """ベクトル検索ツールの作成"""
    try:
        return vector_to_tool()
    except Exception as e:
        logger.error(f"Failed to create vector tool: {str(e)}", exc_info=True)
        raise ToolInitializationError(f"Vector tool initialization failed: {str(e)}")

def initialize_tools() -> List[BaseTool]:
    """環境変数に基づいてツールを初期化"""
    tools = []
    
    # Web検索ツール
    if os.environ.get("ENABLE_SEARCH", "true").lower() == "true":
        try:
            tools.append(create_search_tool())
            logger.info("Web search tool initialized successfully")
        except ToolInitializationError as e:
            logger.warning(f"Skipping web search tool: {str(e)}")
    
    # ベクトル検索ツール
    if os.environ.get("ENABLE_VECTOR", "true").lower() == "true":
        try:
            tools.append(create_vector_tool())
            logger.info("Vector search tool initialized successfully")
        except ToolInitializationError as e:
            logger.warning(f"Skipping vector tool: {str(e)}")
    
    if not tools:
        logger.warning("No tools were initialized!")
    
    return tools

# ツールの初期化
try:
    all_tools = initialize_tools()
    logger.info(f"Initialized {len(all_tools)} tools successfully")
except Exception as e:
    logger.error(f"Failed to initialize tools: {str(e)}", exc_info=True)
    raise
