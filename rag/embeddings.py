from sentence_transformers import SentenceTransformer
from config.constants import EMBEDDING_MODEL

print(f"[embeddings] Loading model: {EMBEDDING_MODEL}")
model = SentenceTransformer(EMBEDDING_MODEL)
print(f"[embeddings] Model ready")


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    print(f"[embeddings] Embedding {len(chunks)} chunks...")
    vectors = model.encode(
        chunks,
        show_progress_bar=True,
        batch_size=32
    ).tolist()
    print(f"[embeddings] Done — vector size: {len(vectors[0])} dims")
    return vectors


def embed_query(query: str) -> list[float]:
    vector = model.encode([query])[0].tolist()
    return vector