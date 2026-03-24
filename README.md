# 📄 AskMyDoc

> An AI-powered RAG document assistant — upload your files and chat with them, powered by Claude and ChromaDB.

---

## ✨ Features

- 📁 **Multi-format support** — Upload PDF, TXT, and DOCX files
- 🧠 **RAG pipeline** — Documents are chunked, embedded, and stored in a local ChromaDB vector store
- 💬 **Conversational chat** — Full multi-turn conversation history maintained per document
- 📌 **Page citations** — Every answer surfaces the source chunks with page numbers and relevance scores
- 🗂️ **Multi-document management** — Index multiple documents and switch between them without losing context
- ⚡ **Streamlit UI** — Clean, responsive interface with sidebar document management

---

## 🏗️ Architecture

```
askmydoc/
├── app.py                  # Streamlit app & chat UI
├── rag/
│   ├── ingestion.py        # File loading & text chunking (PDF, TXT, DOCX)
│   ├── embeddings.py       # Sentence-transformer embeddings
│   ├── vectorstore.py      # ChromaDB vector store operations
│   └── retriever.py        # Similarity search with source filtering
├── llm/
│   └── claude_client.py    # Anthropic Claude API integration
├── config/                 # Configuration & settings
├── requirements.txt
└── .devcontainer/          # Dev container setup
```

**Flow:**
```
Upload File → Chunk → Embed → Store in ChromaDB
                                      ↓
User Question → Embed Query → Retrieve Top Chunks → Claude API → Answer + Citations
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone https://github.com/limbarajjanga-spec/askmydoc.git
cd askmydoc
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

### Run

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| LLM | [Anthropic Claude](https://www.anthropic.com/) |
| Vector Store | [ChromaDB](https://www.trychroma.com/) |
| Embeddings | [Sentence Transformers](https://www.sbert.net/) |
| PDF Parsing | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) |
| DOCX Parsing | [python-docx](https://python-docx.readthedocs.io/) |
| Text Splitting | [LangChain Text Splitters](https://python.langchain.com/) |

---

## 💡 Usage

1. **Upload** a PDF, TXT, or DOCX from the sidebar
2. **Wait** for it to be processed and indexed (chunk count shown)
3. **Ask** any question about the document in the chat
4. **Get** answers with source page numbers and relevance scores
5. **Switch** between indexed documents at any time

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)