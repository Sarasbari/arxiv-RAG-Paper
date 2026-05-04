import chromadb
from config.settings import CHROMA_DIR, COLLECTION_NAME

# singleton client
_client = None
_collection = None


def get_collection():
    """Return (or create) the ChromaDB collection."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def is_paper_indexed(paper_id: str) -> bool:
    """Check if a paper is already in the store."""
    col = get_collection()
    result = col.get(where={"paper_id": paper_id}, limit=1)
    return len(result["ids"]) > 0


def add_chunks(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """
    Insert chunks + embeddings into ChromaDB.
    Returns number of chunks inserted.
    """
    col = get_collection()

    ids, docs, metas = [], [], []
    for chunk, embedding in zip(chunks, embeddings):
        m = chunk["metadata"]
        chunk_id = f"{m['paper_id']}_chunk_{m['chunk_index']}"
        ids.append(chunk_id)
        docs.append(chunk["text"])
        metas.append({
            "paper_id":    m["paper_id"],
            "title":       m["title"],
            "authors":     str(m["authors"]),
            "year":        int(m["year"]),
            "chunk_index": int(m["chunk_index"]),
        })

    if ids:
        # Loophole fix: Batch insert to prevent ChromaDB from throwing payload size limits on huge papers
        batch_size = 500
        for i in range(0, len(ids), batch_size):
            col.add(
                ids=ids[i:i+batch_size], 
                documents=docs[i:i+batch_size], 
                metadatas=metas[i:i+batch_size], 
                embeddings=embeddings[i:i+batch_size]
            )

    return len(ids)


def query_chunks(query_embedding: list[float], top_k: int) -> list[dict]:
    """
    Retrieve top_k most similar chunks.
    Returns list of {text, metadata} dicts.
    """
    col = get_collection()
    results = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text":     doc,
            "metadata": meta,
            "score":    round(1 - dist, 4),  # cosine distance → similarity
        })

    return chunks


def get_stats() -> dict:
    """Return collection stats for the UI sidebar."""
    col = get_collection()
    count = col.count()

    papers = set()
    if count > 0:
        sample = col.get(limit=count, include=["metadatas"])
        for m in sample["metadatas"]:
            papers.add(m.get("paper_id", ""))

    return {"total_chunks": count, "total_papers": len(papers)}