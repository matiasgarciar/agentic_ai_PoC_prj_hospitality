import os
import logging
from typing import Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger("hospitality_api")

# Path to persisted Chroma vectorstore created in Exercise 1
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "rag", "vectorstore")

_system_prompt = """You are a helpful hotel assistant.
Answer using ONLY the provided context.
If the answer is not in the context, say you don't have that information.

Be concise and structured (bullet points/tables when helpful)."""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _system_prompt),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)

_rag_chain = None


def _get_retriever():
    import chromadb

    embeddings = OpenAIEmbeddings(chunk_size=64)

    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    collection_name = os.getenv("CHROMA_COLLECTION", "hotels")

    client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

    vs = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    return vs.as_retriever(search_kwargs={"k": 4})


def _get_chain():
    global _rag_chain
    if _rag_chain is not None:
        return _rag_chain

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriever = _get_retriever()

    def format_docs(docs):
        return "\n\n---\n\n".join(d.page_content for d in docs)

    def invoke(inputs):
        question = inputs["question"]
        docs = retriever.invoke(question)
        context = format_docs(docs)
        return (_prompt | llm).invoke({"question": question, "context": context})

    _rag_chain = invoke
    logger.info("✅ Exercise 1 RAG agent loaded successfully")
    return _rag_chain


def answer_hotel_question_rag(question: str) -> str:
    """Answer a hotel question using RAG over the persisted vectorstore."""
    chain = _get_chain()
    resp = chain({"question": question})
    return resp.content if hasattr(resp, "content") else str(resp)
