# rag/retriever.py
from rag.vectorstore import get_collection
from config.constants import TOP_K_RESULTS


def retrieve_similar_chunks(query_vector: list[float],
                            top_k: int = TOP_K_RESULTS) -> list[dict]:
    """
    Returns list of dicts with text + page + source:
    [
        {"text": "...", "page": 3, "source": "doc.pdf"},
        ...
    ]
    """
    collection = get_collection()

    if collection.count() == 0:
        raise ValueError("No documents in vector store. Upload a PDF first.")

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    enriched = []
    for chunk, meta, dist in zip(chunks, metadatas, distances):
        enriched.append({
            "text": chunk,
            "page": meta.get("page", "?"),
            "source": meta.get("source", "?"),
            "score": round(1 - dist, 3)
        })

    print(f"[retriever] Retrieved {len(enriched)} chunks")
    for i, r in enumerate(enriched):
        print(f"  [{i+1}] page={r['page']} score={r['score']} | {r['text'][:60]}...")

    return enriched