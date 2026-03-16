# app.py
import streamlit as st
import tempfile
import os

from rag.ingestion import load_and_chunk_pdf
from rag.embeddings import embed_chunks, embed_query
from rag.vectorstore import store_chunks, clear_collection, get_collection_count
from rag.retriever import retrieve_similar_chunks
from llm.claude_client import ask_claude

st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 RAG Document Assistant")
st.caption("Upload a PDF and ask questions — powered by Claude")

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Upload Document")
    st.markdown("Supported format: **PDF**")

    uploaded_file = st.file_uploader(
        label="Choose a PDF file",
        type=["pdf"],
        help="Upload the PDF you want to ask questions about"
    )

    if uploaded_file is not None:
        if st.session_state.current_pdf != uploaded_file.name:
            if st.button("Process PDF", type="primary", use_container_width=True):
                with st.spinner("Reading and indexing PDF..."):
                    try:
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".pdf"
                        ) as tmp:
                            tmp.write(uploaded_file.read())
                            tmp_path = tmp.name

                        # Step 1 — Extract text and chunk with page metadata
                        chunks, metadatas = load_and_chunk_pdf(tmp_path)

                        # Step 2 — Embed chunks into vectors
                        vectors = embed_chunks(chunks)

                        # Step 3 — Clear old data, store new vectors
                        clear_collection()
                        store_chunks(chunks, vectors, uploaded_file.name, metadatas)

                        os.unlink(tmp_path)

                        st.session_state.pdf_processed = True
                        st.session_state.current_pdf = uploaded_file.name
                        st.session_state.chat_history = []

                        st.success(f"Indexed {len(chunks)} chunks!")

                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
        else:
            st.success(f"Ready — {get_collection_count()} chunks indexed")

    if st.session_state.pdf_processed:
        st.divider()
        st.markdown(f"**Current doc:**")
        st.markdown(f"`{st.session_state.current_pdf}`")

        if st.button("Clear & Upload New", use_container_width=True):
            clear_collection()
            st.session_state.pdf_processed = False
            st.session_state.current_pdf = None
            st.session_state.chat_history = []
            st.rerun()

if not st.session_state.pdf_processed:
    st.info("Upload a PDF from the sidebar to get started.")

    with st.expander("How it works"):
        st.markdown("""
        1. **Upload** a PDF using the sidebar
        2. **Wait** for it to be processed and indexed
        3. **Ask** any question about the document
        4. **Get** answers grounded in your document with page numbers
        """)
else:
    st.markdown(f"### Ask about `{st.session_state.current_pdf}`")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your document...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("assistant"):
            with st.spinner("Searching document and generating answer..."):
                try:
                    # Step 1 — Embed the question
                    query_vector = embed_query(question)

                    # Step 2 — Retrieve relevant chunks with metadata
                    chunks = retrieve_similar_chunks(query_vector)

                    # Step 3 — Ask Claude with context
                    answer = ask_claude(question, chunks)

                    st.markdown(answer)

                    # Show sources with page numbers
                    with st.expander("View sources"):
                        for i, chunk in enumerate(chunks):
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.markdown(f"**Page {chunk['page']}**")
                                st.caption(f"Score: {chunk['score']}")
                            with col2:
                                st.caption(chunk["text"][:300] + "...")
                            st.divider()

                except Exception as e:
                    answer = f"Error: {str(e)}"
                    st.error(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })