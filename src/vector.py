import os
import logging
from typing import Optional
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool

logger = logging.getLogger(__name__)

def get_vector_store_path() -> Path:
    """ベクトルストアのパスを取得"""
    base_path = Path(os.environ.get("VECTOR_STORE_PATH", "./vector_store"))
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path

def load_documents(file_path: str, chunk_config: Optional[dict] = None) -> list:
    """ドキュメントの読み込みと分割"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    try:
        raw_documents = TextLoader(file_path).load()
        
        # チャンク設定
        default_config = {
            "chunk_size": int(os.environ.get("VECTOR_CHUNK_SIZE", "100")),
            "chunk_overlap": int(os.environ.get("VECTOR_CHUNK_OVERLAP", "20")),
            "separator": os.environ.get("VECTOR_CHUNK_SEPARATOR", "\\n"),
        }
        config = {**default_config, **(chunk_config or {})}
        
        text_splitter = CharacterTextSplitter(**config)
        return text_splitter.split_documents(raw_documents)
    
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}", exc_info=True)
        raise

def initialize_vector_store(documents: list, persist_directory: Path) -> Chroma:
    """ベクトルストアの初期化"""
    try:
        embeddings = OpenAIEmbeddings(
            timeout=float(os.environ.get("OPENAI_TIMEOUT", "30")),
            max_retries=int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
        )
        
        # 永続化ディレクトリを指定してChromaDBを初期化
        return Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=str(persist_directory),
            collection_name="work_rules"
        )
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}", exc_info=True)
        raise

def vector_to_tool(
    file_path: Optional[str] = None,
    chunk_config: Optional[dict] = None,
) -> create_retriever_tool:
    """ベクトル検索ツールの作成"""
    try:
        # ドキュメントファイルのパス
        doc_path = file_path or os.environ.get("VECTOR_DOC_PATH", "./vector_file/sample.txt")
        
        # ベクトルストアのパス
        persist_dir = get_vector_store_path()
        
        # ドキュメントの読み込みと分割
        documents = load_documents(doc_path, chunk_config)
        
        # ベクトルストアの初期化（永続化ディレクトリを指定）
        vectorstore = initialize_vector_store(documents, persist_dir)
        
        # 検索ツールの作成
        return create_retriever_tool(
            retriever=vectorstore.as_retriever(
                search_kwargs={
                    "k": int(os.environ.get("VECTOR_SEARCH_K", "4")),
                }
            ),
            name="vector_search",
            description="社内規則や文書に関する質問に答えるために使用します。質問に関連する情報を検索して提供します。",
        )
    
    except Exception as e:
        logger.error(f"Error creating vector tool: {str(e)}", exc_info=True)
        raise
