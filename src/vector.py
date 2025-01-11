from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool


def vector_to_tool():
    raw_documents = TextLoader("./vector_file/sample.txt").load()
    text_splitter = CharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=0,
        separator="\\n",
    )
    documents = text_splitter.split_documents(raw_documents)
    vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())

    return create_retriever_tool(
        retriever=vectorstore.as_retriever(),
        name="WorkRules",
        description="Use this tool when answering questions about work rules.",
    )
