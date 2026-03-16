# rag/vectorstore.py
import chromadb
from config.constants import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR

client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def get_collection():
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def store_chunks(chunks: list[str],
                 vectors: list[list[float]],
                 doc_name: str,
                 metadatas: list[dict] = None):
    collection = get_collection()

    ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]

    if metadatas:
        enriched = [
            {"source": doc_name, "page": m.get("page", 0)}
            for m in metadatas
        ]
    else:
        enriched = [
            {"source": doc_name, "page": 0}
            for _ in chunks
        ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=vectors,
        metadatas=enriched
    )
    print(f"[vectorstore] Stored {len(chunks)} chunks from '{doc_name}'")


def clear_collection():
    try:
        client.delete_collection(name=CHROMA_COLLECTION_NAME)
        print(f"[vectorstore] Collection cleared")
    except Exception:
        pass


def get_collection_count() -> int:
    collection = get_collection()
    return collection.count()