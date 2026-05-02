from pathlib import Path

# ── Paths ────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
PAPERS_DIR   = BASE_DIR / "papers"
CHROMA_DIR   = BASE_DIR / "chroma_db"

PAPERS_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# ── ChromaDB ─────────────────────────────────────────────
COLLECTION_NAME = "research_papers"

# ── Embedding (Ollama local — free) ──────────────────────
EMBED_MODEL     = "nomic-embed-text"
EMBED_DIM       = 768

# ── Retrieval ────────────────────────────────────────────
TOP_K           = 12      # chunks retrieved per query
MIN_SCORE       = 0.0     # future: filter low-relevance chunks

# ── Ingestion ────────────────────────────────────────────
DEFAULT_FETCH_COUNT          = 20    # papers per arxiv query
CHUNK_BREAKPOINT_PERCENTILE  = 92    # higher = bigger chunks
CHUNK_BUFFER_SIZE            = 1

# ── Claude API ───────────────────────────────────────────
CLAUDE_MODEL    = "claude-opus-4-5"
MAX_TOKENS      = 1500

# ── Default arxiv topics to seed the knowledge base ──────
DEFAULT_TOPICS = [
    "RAG retrieval augmented generation LLM",
    "semantic chunking document splitting embeddings",
    "vector database similarity search FAISS",
    "large language model prompting techniques",
    "dense retrieval passage ranking transformers",
]