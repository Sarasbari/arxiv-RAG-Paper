# arXiv RAG Paper

A Retrieval-Augmented Generation (RAG) pipeline for querying arXiv research papers using Claude, ChromaDB, and Ollama embeddings.

## Architecture

```
arxiv API → PDF download → text extraction → semantic chunking → embedding → ChromaDB
                                                                                 ↓
                                              Claude API ← reranked chunks ← vector search ← user query
```

## Quick Start

```bash
# Install dependencies
make install

# Set your API key
echo "ANTHROPIC_API_KEY=sk-..." > .env

# Ingest papers
make ingest

# Launch the UI
make run
```

## Project Structure

- **`core/`** — Pure functions, no side effects (fetcher, extractor, chunker, embedder, vectorstore)
- **`pipeline/`** — Orchestration layer that calls core modules (ingest, query, synthesizer)
- **`app/`** — Streamlit UI (entry point + components)
- **`config/`** — Zero logic, only values (settings + prompts)
- **`tests/`** — Unit tests for chunker and query pipeline

## Testing

```bash
make test
```

## Tech Stack

| Component   | Tool                  |
|-------------|-----------------------|
| LLM         | Claude (Anthropic)    |
| Embeddings  | nomic-embed (Ollama)  |
| Vector DB   | ChromaDB              |
| Chunking    | LlamaIndex            |
| PDF Parsing | pypdf                 |
| UI          | Streamlit             |
