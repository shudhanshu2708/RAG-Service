# RAG-Service

A Retrieval-Augmented Generation (RAG) backend that lets you upload PDF documents and ask natural-language questions about their content. Built with FastAPI, LangChain, ChromaDB, and Ollama for fully local inference (no external API keys required).

## How it works

```
PDF Upload → Text Extraction → Chunking → Embeddings → ChromaDB (vector store)
                                                              ↓
User Question → Semantic Retrieval → Context + Question → LLM → Answer
```

1. **Upload** — a PDF is parsed and its text extracted using `pypdf`.
2. **Chunking** — text is split into overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`, so context isn't lost at chunk boundaries.
3. **Embedding & storage** — each chunk is embedded (`nomic-embed-text` via Ollama) and stored in a persistent ChromaDB vector store.
4. **Retrieval** — when a question comes in, the most semantically relevant chunks are retrieved from ChromaDB.
5. **Generation** — the retrieved chunks are passed as context to a local LLM (`llama3.2:3b` via Ollama) using an LCEL (LangChain Expression Language) pipeline, which generates a grounded answer.

## Tech Stack

- **Backend:** FastAPI
- **LLM & Embeddings:** Ollama (`llama3.2:3b`, `nomic-embed-text`) — runs fully locally
- **Orchestration:** LangChain (LCEL-based retrieval chain)
- **Vector Store:** ChromaDB
- **PDF Parsing:** pypdf
- **Frontend:** Vanilla HTML/CSS/JS (no build step), served directly by FastAPI

## Project Structure

```
RAG-Service/
├── app/
│   ├── main.py              # FastAPI app, upload/count endpoints, chunking logic
│   ├── routes/
│   │   └── ask.py           # /ask endpoint — retrieval + generation pipeline
│   └── core/
│       └── vectorstore.py   # ChromaDB + embeddings setup
├── static/
│   └── index.html           # Minimal upload + ask UI
├── uploads/                 # Uploaded PDFs (gitignored)
├── chroma_db/                # Persisted vector store (gitignored)
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally

### 1. Clone and set up a virtual environment
```bash
git clone https://github.com/shudhanshu2708/RAG-Service.git
cd RAG-Service
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Pull the required Ollama models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

### 5. Open the app
Visit `http://127.0.0.1:8000/` in your browser for the upload + ask UI, or `http://127.0.0.1:8000/docs` for the interactive Swagger API docs.

## API Endpoints

| Method | Endpoint  | Description                                  |
|--------|-----------|-----------------------------------------------|
| GET    | `/`       | Serves the frontend UI                        |
| POST   | `/upload` | Upload a PDF; extracts, chunks, and stores it  |
| GET    | `/count`  | Returns total number of chunks stored          |
| POST   | `/ask`    | Ask a question; returns an answer + sources    |

**Example — `/ask` request body:**
```json
{ "question": "What is the main topic of the document?" }
```

**Example — `/ask` response:**
```json
{
  "answer": "...",
  "sources": [{ "source": "example.pdf", "chunk_index": 3 }]
}
```

## Status

🚧 Actively being built. Currently supports single-document PDF Q&A with a basic local UI. Planned next steps include multi-document support and improved retrieval tuning.

## License

MIT
