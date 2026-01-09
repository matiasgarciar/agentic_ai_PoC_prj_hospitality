import os
import chromadb

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def load_docs():
    base = os.path.join(os.path.dirname(__file__), "..", "..", "data", "hotels")
    hotels_json = os.path.join(base, "hotels.json")
    details_md = os.path.join(base, "hotel_details.md")

    docs = []
    if os.path.exists(hotels_json):
        with open(hotels_json, "r", encoding="utf-8") as f:
            docs.append(Document(page_content=f.read(), metadata={"source": "hotels.json"}))
    if os.path.exists(details_md):
        with open(details_md, "r", encoding="utf-8") as f:
            docs.append(Document(page_content=f.read(), metadata={"source": "hotel_details.md"}))
    return docs


def main():
    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    collection_name = os.getenv("CHROMA_COLLECTION", "hotels")

    client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

    embeddings = OpenAIEmbeddings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)

    docs = load_docs()
    splits = splitter.split_documents(docs)

    # Rebuild cleanly
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    vs = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )
    vs.add_documents(splits)

    print(f"✅ Indexed {len(splits)} chunks into collection '{collection_name}' on {chroma_host}:{chroma_port}")


if __name__ == "__main__":
    main()
