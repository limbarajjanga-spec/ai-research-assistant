# rag/ingestion.py
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.constants import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text page by page and returns list of dicts
    with text + page number.

    Returns:
        [{"text": "...", "page": 1}, {"text": "...", "page": 2}, ...]
    """
    doc = fitz.open(file_path)
    pages = []
    num_pages = len(doc)

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # skip empty pages
            pages.append({
                "text": text,
                "page": page_num + 1  # 1-indexed for humans
            })

    doc.close()
    print(f"[ingestion] Extracted {num_pages} pages")
    return pages


def chunk_text_with_metadata(pages: list[dict]) -> tuple[list[str], list[dict]]:
    """
    Chunks each page's text and tracks which page each chunk came from.

    Returns:
        chunks:    list of text strings
        metadatas: list of dicts with page number and source info
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []
    all_metadatas = []

    for page_data in pages:
        page_chunks = splitter.split_text(page_data["text"])

        for chunk in page_chunks:
            if chunk.strip():
                all_chunks.append(chunk.strip())
                all_metadatas.append({
                    "page": page_data["page"]
                })

    print(f"[ingestion] Created {len(all_chunks)} chunks with page metadata")
    return all_chunks, all_metadatas


def load_and_chunk_pdf(file_path: str) -> tuple[list[str], list[dict]]:
    """
    Main function called by app.py.

    Returns:
        chunks:    list of text strings
        metadatas: list of dicts {"page": N}
    """
    pages = extract_text_from_pdf(file_path)

    if not pages:
        raise ValueError(f"No text found in PDF: {file_path}. "
                         "It may be a scanned image-only PDF.")

    chunks, metadatas = chunk_text_with_metadata(pages)
    return chunks, metadatas