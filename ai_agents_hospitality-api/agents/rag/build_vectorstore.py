import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "../../../bookings-db/output_files/hotels"
PERSIST_DIR = "./vectorstore"


def load_documents():
    docs = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".md"):
            loader = TextLoader(os.path.join(DATA_DIR, fname), encoding="utf-8")
            docs.extend(loader.load())
    return docs


def main():
    documents = load_documents()
    if not documents:
        raise RuntimeError(f"No .md documents found in {DATA_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(chunk_size=64)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )

    print(f"✅ Vectorstore created with {len(chunks)} chunks at {PERSIST_DIR}")


if __name__ == "__main__":
    main()
