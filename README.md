# arXiv RAG Paper

A Retrieval-Augmented Generation (RAG) pipeline for querying arXiv research papers using Gemini, ChromaDB, and sentence-transformers.

## Architecture

```
arxiv API → PDF download → text extraction → semantic chunking → embedding → ChromaDB
                                                                                 ↓
                                              Gemini API ← reranked chunks ← vector search ← user query
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key (free from https://aistudio.google.com/apikey)
echo "GEMINI_API_KEY=your_key_here" > .env

# Ingest papers
python -m pipeline.ingest_pipeline

# Launch the UI
streamlit run app/main.py
```

## Project Structure

- **`core/`** — Pure functions, no side effects (fetcher, extractor, chunker, embedder, vectorstore)
- **`pipeline/`** — Orchestration layer that calls core modules (ingest, query, synthesizer)
- **`app/`** — Streamlit UI (entry point + components)
- **`config/`** — Zero logic, only values (settings + prompts)
- **`tests/`** — Unit tests for chunker and query pipeline

## Testing

```bash
pytest tests/ -v
```

## Tech Stack

| Component   | Tool                          |
|-------------|-------------------------------|
| LLM         | Gemini Flash (Google, free)   |
| Embeddings  | all-MiniLM-L6-v2 (local)     |
| Vector DB   | ChromaDB                      |
| Chunking    | LlamaIndex                    |
| PDF Parsing | pypdf                         |
| UI          | Streamlit                     |
