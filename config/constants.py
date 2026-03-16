# config/constants.py
# -------------------
# All magic numbers and model settings live here.
# To tune the RAG pipeline, you only touch this file — nothing else.

# ── PDF Chunking ──────────────────────────────────────────
CHUNK_SIZE = 1000        # Number of characters per chunk
CHUNK_OVERLAP = 100      # Overlap between chunks to preserve context

# ── Embedding Model ───────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # Free, local, no API key needed

# ── ChromaDB ──────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "pdf_documents"
CHROMA_PERSIST_DIR = "./chroma_store"   # Where vectors are saved on disk

# ── Retrieval ─────────────────────────────────────────────
TOP_K_RESULTS = 8       # How many chunks to retrieve per query

# ── Claude LLM ────────────────────────────────────────────
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 1024